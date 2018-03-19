'''
Created on Sep 10, 2017

@author: Richard Christie
'''

import os, sys
import json
from PySide import QtGui, QtCore

from opencmiss.zinc.context import Context
from opencmiss.zinc.result import RESULT_OK
from opencmiss.zinc.field import Field
from opencmiss.zinc.glyph import Glyph
from opencmiss.zinc.graphics import Graphics
from opencmiss.zinc.material import Material
from opencmiss.zinc.node import Node
from opencmiss.zinc.optimisation import Optimisation
from mapclientplugins.meshmergerstep.utils import zinc as zincutils

STRING_FLOAT_FORMAT = '{:.8g}'

class MeshMergerModel(object):
    '''
    Framework for generating meshes of a number of types, with mesh type specific options
    '''

    def __init__(self):
        '''
        Constructor, to be followed by configure().
        '''
        self._location = None
        self._identifier = None
        self._filenameStem = None
        self._context = Context("MeshMerger")
        self._masterRegion = None
        self._slaveRegion = None
        self._masterFilename = None
        self._slaveFilename = None
        tess = self._context.getTessellationmodule().getDefaultTessellation()
        tess.setRefinementFactors(12)
        self._sceneChangeCallback = None
        # set up standard materials and glyphs so we can use them elsewhere
        self._materialmodule = self._context.getMaterialmodule()
        self._materialmodule.defineStandardMaterials()
        solid_blue = self._materialmodule.createMaterial()
        solid_blue.setName('solid_blue')
        solid_blue.setManaged(True)
        solid_blue.setAttributeReal3(Material.ATTRIBUTE_AMBIENT, [ 0.0, 0.2, 0.6 ])
        solid_blue.setAttributeReal3(Material.ATTRIBUTE_DIFFUSE, [ 0.0, 0.7, 1.0 ])
        solid_blue.setAttributeReal3(Material.ATTRIBUTE_EMISSION, [ 0.0, 0.0, 0.0 ])
        solid_blue.setAttributeReal3(Material.ATTRIBUTE_SPECULAR, [ 0.1, 0.1, 0.1 ])
        solid_blue.setAttributeReal(Material.ATTRIBUTE_SHININESS , 0.2)
        trans_blue = self._materialmodule.createMaterial()
        trans_blue.setName('trans_blue')
        trans_blue.setManaged(True)
        trans_blue.setAttributeReal3(Material.ATTRIBUTE_AMBIENT, [ 0.0, 0.2, 0.6 ])
        trans_blue.setAttributeReal3(Material.ATTRIBUTE_DIFFUSE, [ 0.0, 0.7, 1.0 ])
        trans_blue.setAttributeReal3(Material.ATTRIBUTE_EMISSION, [ 0.0, 0.0, 0.0 ])
        trans_blue.setAttributeReal3(Material.ATTRIBUTE_SPECULAR, [ 0.1, 0.1, 0.1 ])
        trans_blue.setAttributeReal(Material.ATTRIBUTE_ALPHA , 0.3)
        trans_blue.setAttributeReal(Material.ATTRIBUTE_SHININESS , 0.2)
        glyphmodule = self._context.getGlyphmodule()
        glyphmodule.defineStandardGlyphs()
        self._isMerged = False
        self._isFitted = False
        self._mergeNodes = {}
        self._settings = {
            'mergeNodes' : '',
            'previewMerge' : True,
            'fit' : False,
            'previewFit' : False,
            'displayAxes' : True,
            'displayElementNumbers' : True,
            'displayLines' : True,
            'displayNodeDerivatives' : False,
            'displayNodeNumbers' : True,
            'displaySurfaces' : True,
            'displaySurfacesExterior' : True,
            'displaySurfacesTranslucent' : True,
            'displaySurfacesWireframe' : False,
            'displayXiAxes' : False
        }

    def configure(self, location, identifier, masterFilename, slaveFilename):
        '''
        Second part of construction, separated to catch exceptions for missing files.
        '''
        self._location = location
        self._identifier = identifier
        self._filenameStem = os.path.join(self._location, self._identifier)
        self._masterRegion = self._context.createRegion()
        self._masterRegion.setName("Master")
        self._slaveRegion = self._context.createRegion()
        self._slaveRegion.setName("Slave")
        self._masterFilename = masterFilename
        self._slaveFilename = slaveFilename
        self._loadSettings()

        result = self._slaveRegion.readFile(self._slaveFilename)
        if result != RESULT_OK:
            self._writeLogMessages()
            raise IOError('Failed to read slave file ' + self._slaveFilename)
        self._createGraphics(self._slaveRegion)

        if self._settings['previewMerge'] and (len(self._mergeNodes) > 0):
            # _mergeMesh reads the master mesh and creates graphics
            self._mergeMesh()
        else:
            result = self._masterRegion.readFile(self._masterFilename)
            if result != RESULT_OK:
                self._writeLogMessages()
                raise IOError('Failed to read master file ' + self._masterFilename)
            self._createGraphics(self._masterRegion)

    def _writeLogMessages(self):
        logger = self._context.getLogger()
        loggerMessageCount = logger.getNumberOfMessages()
        if loggerMessageCount > 0:
            for i in range(1, loggerMessageCount + 1):
                print(logger.getMessageTypeAtIndex(i), logger.getMessageTextAtIndex(i))
            logger.removeAllMessages()

    def getMergeNodesText(self):
        return self._settings['mergeNodes']

    def setMergeNodesText(self, mergeNodesText):
        self._parseMergeNodesText(mergeNodesText)
        if self.isPreviewMerge():
            self._mergeMesh()

    def checkMasterNodeId(self, masterNodeId):
        masterNodes = self._masterRegion.getFieldmodule().findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
        masterNode = masterNodes.findNodeByIdentifier(masterNodeId)
        return masterNode.isValid()

    def checkSlaveNodeId(self, slaveNodeId):
        slaveNodes = self._slaveRegion.getFieldmodule().findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
        slaveNode = slaveNodes.findNodeByIdentifier(slaveNodeId)
        return slaveNode.isValid()

    def selectMasterNodeId(self, masterNodeId):
        '''
        Ensure the graphical selection for the master scene is cleared and just the supplied node selected.
        :masterNodeId: Identifier of node to select, or None to only clear.
        '''
        nodes = self._masterRegion.getFieldmodule().findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
        node = nodes.findNodeByIdentifier(masterNodeId) if (masterNodeId is not None) else None
        zincutils.selectRegionNode(self._masterRegion, node)

    def selectSlaveNodeId(self, slaveNodeId):
        '''
        Ensure the graphical selection for the slave scene is cleared and just the supplied node selected.
        :slaveNodeId: Identifier of node to select, or None to only clear.
        '''
        nodes = self._slaveRegion.getFieldmodule().findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
        node = nodes.findNodeByIdentifier(slaveNodeId) if (slaveNodeId is not None) else None
        zincutils.selectRegionNode(self._slaveRegion, node)

    def findMergeSlaveNodeId(self, masterNodeId):
        '''
        Get slave node for master node, if exists, otherwise None.
        :masterNodeId:  Identifier of master node to match.
        '''
        return self._mergeNodes.get(masterNodeId)

    def _makeMergeNodesText(self):
        mergeNodesText = ''
        for masterNodeId in sorted(self._mergeNodes.keys()):
            mergeNodesText += str(masterNodeId) + '=' + str(self._mergeNodes[masterNodeId]) + '\n'
        self._settings['mergeNodes'] = mergeNodesText

    def _parseMergeNodesText(self, mergeNodesText):
        self._mergeNodes = {}
        for s in mergeNodesText.split():
            try:
                ends = s.split('=')
                self._mergeNodes[int(ends[0])] = int(ends[1])
            except:
                pass
        self._makeMergeNodesText()

    def mergeNodes(self, masterNodeId, slaveNodeId):
        '''
        :return:  True if valid and changing, otherwise False.
        '''
        if not (self.checkMasterNodeId(masterNodeId) and self.checkSlaveNodeId(slaveNodeId)):
            return False
        if slaveNodeId == self._mergeNodes.get(masterNodeId):
            return False
        self._mergeNodes[masterNodeId] = slaveNodeId
        self._makeMergeNodesText()
        if self.isPreviewMerge():
            self._mergeMesh()
        return True

    def deleteMergeNode(self, masterNodeId):
        if masterNodeId in self._mergeNodes:
            self._mergeNodes.pop(masterNodeId)
            self._makeMergeNodesText()
            if self.isPreviewMerge():
                self._mergeMesh()
            return True
        return False

    def getContext(self):
        return self._context

    def getMasterRegion(self):
        return self._masterRegion

    def getSlaveRegion(self):
        return self._slaveRegion

    def registerSceneChangeCallback(self, sceneChangeCallback):
        self._sceneChangeCallback = sceneChangeCallback

    def getMasterScene(self):
        return self._masterRegion.getScene()

    def getSlaveScene(self):
        return self._slaveRegion.getScene()

    def getIdentifier(self):
        return self._identifier

    def _loadSettings(self):
        try:
            with open(self._filenameStem + '-settings.json', 'r') as f:
                self._settings.update(json.loads(f.read()))
            self._parseMergeNodesText(self._settings['mergeNodes'])
        except FileNotFoundError:
            pass  # no settings saved yet

    def _saveSettings(self):
        with open(self._filenameStem + '-settings.json', 'w') as f:
            f.write(json.dumps(self._settings, default=lambda o: o.__dict__, sort_keys=True, indent=4))

    def isPreviewMerge(self):
        return self._settings['previewMerge']

    def setPreviewMerge(self, previewMerge):
        self._settings['previewMerge'] = previewMerge
        self._mergeMesh()

    def isFit(self):
        return self._settings['fit']

    def setFit(self, fit):
        self._settings['fit'] = fit
        if self.isPreviewFit():
            self._mergeMesh()

    def isPreviewFit(self):
        return self._settings['previewFit']

    def setPreviewFit(self, previewFit):
        self._settings['previewFit'] = previewFit
        if self.isFit():
            self._mergeMesh()

    def _getVisibility(self, graphicsName):
        return self._settings[graphicsName]

    def _setVisibility(self, graphicsName, show):
        self._settings[graphicsName] = show
        graphics = self.getMasterScene().findGraphicsByName(graphicsName)
        graphics.setVisibilityFlag(show)
        graphics = self.getSlaveScene().findGraphicsByName(graphicsName)
        graphics.setVisibilityFlag(show)

    def isDisplayAxes(self):
        return self._getVisibility('displayAxes')

    def setDisplayAxes(self, show):
        self._setVisibility('displayAxes', show)

    def isDisplayElementNumbers(self):
        return self._getVisibility('displayElementNumbers')

    def setDisplayElementNumbers(self, show):
        self._setVisibility('displayElementNumbers', show)

    def isDisplayLines(self):
        return self._getVisibility('displayLines')

    def setDisplayLines(self, show):
        self._setVisibility('displayLines', show)

    def isDisplayNodeDerivatives(self):
        return self._getVisibility('displayNodeDerivatives')

    def setDisplayNodeDerivatives(self, show):
        graphicsName = 'displayNodeDerivatives'
        self._settings[graphicsName] = show
        for scene in [self.getMasterScene(), self.getSlaveScene()]:
            graphics = scene.getFirstGraphics()
            while graphics.isValid():
                if graphics.getName() == graphicsName:
                    graphics.setVisibilityFlag(show)
                graphics = scene.getNextGraphics(graphics)

    def isDisplayNodeNumbers(self):
        return self._getVisibility('displayNodeNumbers')

    def setDisplayNodeNumbers(self, show):
        self._setVisibility('displayNodeNumbers', show)

    def isDisplaySurfaces(self):
        return self._getVisibility('displaySurfaces')

    def setDisplaySurfaces(self, show):
        self._setVisibility('displaySurfaces', show)

    def isDisplaySurfacesExterior(self):
        return self._settings['displaySurfacesExterior']

    def setDisplaySurfacesExterior(self, isExterior):
        self._settings['displaySurfacesExterior'] = isExterior
        for region in (self._masterRegion, self._slaveRegion):
            surfaces = region.getScene().findGraphicsByName('displaySurfaces')
            surfaces.setExterior(self.isDisplaySurfacesExterior() if (self.getMeshDimension(region) == 3) else False)

    def isDisplaySurfacesTranslucent(self):
        return self._settings['displaySurfacesTranslucent']

    def setDisplaySurfacesTranslucent(self, isTranslucent):
        self._settings['displaySurfacesTranslucent'] = isTranslucent
        for region in (self._masterRegion, self._slaveRegion):
            surfaces = region.getScene().findGraphicsByName('displaySurfaces')
            surfacesMaterial = self._materialmodule.findMaterialByName('trans_blue' if isTranslucent else 'solid_blue')
            surfaces.setMaterial(surfacesMaterial)

    def isDisplaySurfacesWireframe(self):
        return self._settings['displaySurfacesWireframe']

    def setDisplaySurfacesWireframe(self, isWireframe):
        self._settings['displaySurfacesWireframe'] = isWireframe
        for region in (self._masterRegion, self._slaveRegion):
            surfaces = region.getScene().findGraphicsByName('displaySurfaces')
            surfaces.setRenderPolygonMode(Graphics.RENDER_POLYGON_MODE_WIREFRAME if isWireframe else Graphics.RENDER_POLYGON_MODE_SHADED)

    def isDisplayXiAxes(self):
        return self._getVisibility('displayXiAxes')

    def setDisplayXiAxes(self, show):
        self._setVisibility('displayXiAxes', show)

    def _getMesh(self, region):
        fm = region.getFieldmodule()
        for dimension in range(3,0,-1):
            mesh = fm.findMeshByDimension(dimension)
            if mesh.getSize() > 0:
                break
        if mesh.getSize() == 0:
            mesh = fm.findMeshByDimension(3)
        return mesh

    def getMeshDimension(self, region):
        return self._getMesh(region).getDimension()

    def _mergeMesh(self, force = False):
        self._isMerged = False
        self._isFitted = False
        self._masterRegion.setName("Old Master")
        self._masterRegion = self._context.createRegion()
        self._masterRegion.setName("New Master")
        result = self._masterRegion.readFile(self._masterFilename)
        if result != RESULT_OK:
            self._writeLogMessages()
            raise IOError('Failed to read master file ' + self._masterFilename + ' during merge')
 
        if (len(self._mergeNodes) > 0) and (force or self.isPreviewMerge()):
            # perform merge of slave into master
            masterFm = self._masterRegion.getFieldmodule()
            masterNodes = masterFm.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
            maximumMasterNodeId = zincutils.getMaximumNodeId(masterNodes)
            masterCoordinates = masterFm.findFieldByName('coordinates').castFiniteElement()
            masterCache = masterFm.createFieldcache()
            masterMesh = self._getMesh(self._masterRegion)
            masterMeshDimension = masterMesh.getDimension()
            # make group of original master nodes and elements for later fitting
            fieldTrue = masterFm.createFieldConstant([1])
            origMasterNodeGroup = masterFm.createFieldNodeGroup(masterNodes)
            origMasterNodesetGroup = origMasterNodeGroup.getNodesetGroup()
            origMasterNodesetGroup.addNodesConditional(fieldTrue)
            origMasterElementGroup = masterFm.createFieldElementGroup(masterMesh)
            origMasterMeshGroup = origMasterElementGroup.getMeshGroup()
            origMasterMeshGroup.addElementsConditional(fieldTrue)
            # modify copy of slave region
            slaveRegion = self._context.createRegion()
            slaveRegion.setName("Merge Slave")
            slaveRegion.readFile(self._slaveFilename)
            slaveFm = slaveRegion.getFieldmodule()
            slaveNodes = slaveFm.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
            maximumSlaveNodeId = zincutils.getMaximumNodeId(slaveNodes)
            # make reference slave coordinates for fitting, using trick of renaming coordinates and reloading
            slaveReferenceCoordinatesName = 'slave_reference_coordinates'
            slaveCoordinates = slaveFm.findFieldByName('coordinates').castFiniteElement()
            slaveCoordinates.setName(slaveReferenceCoordinatesName)
            slaveRegion.readFile(self._slaveFilename)
            slaveCoordinates = slaveFm.findFieldByName('coordinates').castFiniteElement()
            # note: can't handle mix of component counts
            componentCount = slaveCoordinates.getNumberOfComponents()
            slaveCache = slaveFm.createFieldcache()
            slaveMesh = self._getMesh(slaveRegion)
            slaveMeshDimension = slaveMesh.getDimension()
            # get mean translation from matched slave to master nodes
            cache = slaveFm.createFieldcache()
            count = 0
            # create matched group for optimising orientation
            slaveFm.beginChange()
            slaveMatchedNodesField = slaveFm.createFieldNodeGroup(slaveNodes)
            slaveMatchedNodesGroup = slaveMatchedNodesField.getNodesetGroup()
            slaveMasterCoordinates = slaveFm.createFieldFiniteElement(componentCount)
            nodetemplate = slaveNodes.createNodetemplate()
            nodetemplate.defineField(slaveMasterCoordinates)
            masterMeanX = [0.0]*componentCount
            slaveMeanX = [0.0]*componentCount
            for masterNodeId, slaveNodeId in self._mergeNodes.items():
                masterNode = masterNodes.findNodeByIdentifier(masterNodeId)
                masterCache.setNode(masterNode)
                result, masterX = masterCoordinates.evaluateReal(masterCache, componentCount)
                #print('master ', masterNodeId,'result',result,masterX)
                slaveNode = slaveNodes.findNodeByIdentifier(slaveNodeId)
                slaveNode.merge(nodetemplate)
                slaveMatchedNodesGroup.addNode(slaveNode)
                slaveCache.setNode(slaveNode)
                result, slaveX = slaveCoordinates.evaluateReal(slaveCache, componentCount)
                #print(' slave ', slaveNodeId,'result',result,slaveX)
                result = slaveMasterCoordinates.assignReal(slaveCache, masterX)
                for c in range(componentCount):
                    masterMeanX[c] += masterX[c]
                    slaveMeanX[c] += slaveX[c]
                count += 1
            # take the mean
            for c in range(componentCount):
                masterMeanX[c] /= count
                slaveMeanX[c] /= count

            masterMinusMeanX = [-x for x in masterMeanX]
            slaveMinusMeanX = [-x for x in slaveMeanX]
            # translate coordinates so means on matched nodes are at zero
            zincutils.translateNodeCoordinates(slaveNodes, slaveCoordinates, slaveMinusMeanX)
            zincutils.translateNodeCoordinates(slaveMatchedNodesGroup, slaveMasterCoordinates, masterMinusMeanX)

            # offset slave node identifier so not clashing with current and future master/merged nodes
            idOffset = maximumMasterNodeId + maximumSlaveNodeId
            zincutils.offsetNodeIds(slaveNodes, idOffset)

            # give merged nodes same id as master, offset remaining slave node ids to be above master node ids
            slaveCache = slaveFm.createFieldcache()
            slaveNodeIdMaps = []
            nextNewId = maximumMasterNodeId + 1
            nodeiterator = slaveNodes.createNodeiterator()
            node = nodeiterator.next()
            while node.isValid():
                oldId = node.getIdentifier()
                newId = -1
                for masterNodeId, slaveNodeId in self._mergeNodes.items():
                    if oldId == (slaveNodeId + idOffset):
                        newId = masterNodeId
                        break;
                if newId < 0:
                    newId = nextNewId
                    nextNewId += 1
                slaveNodeIdMaps.append((oldId, newId))
                node = nodeiterator.next()
            for idMap in slaveNodeIdMaps:
                node = slaveNodes.findNodeByIdentifier(idMap[0])
                node.setIdentifier(idMap[1])

            # non-linear optimisation to rotate slave nodes onto master coordinates
            azimuth = slaveFm.createFieldConstant([0.0])
            elevation = slaveFm.createFieldConstant([0.0])
            roll = slaveFm.createFieldConstant([0.0])
            rotationMatrix = zincutils.createRotationMatrixField(azimuth, elevation, roll)
            rotatedSlaveCoordinates = slaveFm.createFieldMatrixMultiply(3, rotationMatrix, slaveCoordinates)
            #print('rotatedSlaveCoordinates.isValid() =',rotatedSlaveCoordinates.isValid())
            delta = slaveFm.createFieldSubtract(rotatedSlaveCoordinates, slaveMasterCoordinates)
            error = slaveFm.createFieldMagnitude(delta)
            alignObjective = slaveFm.createFieldNodesetSum(error, slaveMatchedNodesGroup)
            #print('alignObjective.isValid() =', alignObjective.isValid(), '#nodes=', slaveMatchedNodesGroup.getSize())
            #result, matrixBefore = rotationMatrix.evaluateReal(slaveCache, 9)
            #print(result, 'matrixBefore', matrixBefore)
            result, alignObjectiveBefore = alignObjective.evaluateReal(slaveCache, 1)
            #print(result, 'alignObjectiveBefore', alignObjectiveBefore)
            eulerAngles = slaveFm.createFieldConcatenate([azimuth, elevation, roll])
            result, eulerAnglesBefore = eulerAngles.evaluateReal(slaveCache, 3)
            #print(result, 'eulerAnglesBefore', eulerAnglesBefore)

            alignOptimisation = slaveFm.createOptimisation()
            alignOptimisation.setMethod(Optimisation.METHOD_QUASI_NEWTON)
            alignOptimisation.setAttributeInteger(Optimisation.ATTRIBUTE_MAXIMUM_ITERATIONS, 100)
            alignOptimisation.setAttributeInteger(Optimisation.ATTRIBUTE_MAXIMUM_FUNCTION_EVALUATIONS, 1000)
            alignOptimisation.setAttributeReal(Optimisation.ATTRIBUTE_FUNCTION_TOLERANCE, 1.0e-8)  # 1.0e-8
            alignOptimisation.addObjectiveField(alignObjective)
            alignOptimisation.addIndependentField(azimuth)
            alignOptimisation.addIndependentField(elevation)
            alignOptimisation.addIndependentField(roll)

            result = alignOptimisation.optimise()
            #print('alignOptimisation result =', result)
            #report = alignOptimisation.getSolutionReport()
            #print(report)

            result, matrixAfter = rotationMatrix.evaluateReal(slaveCache, 9)
            #print(result, 'matrixAfter', matrixAfter)
            result, alignObjectiveAfter = alignObjective.evaluateReal(slaveCache, 1)
            #print(result, 'alignObjectiveAfter', alignObjectiveAfter)
            result, eulerAnglesAfter = eulerAngles.evaluateReal(slaveCache, 3)
            #print(result, 'eulerAnglesAfter', eulerAnglesAfter)

            zincutils.transformNodeCoordinates(slaveNodes, slaveCoordinates, matrixAfter, masterMeanX)

            # release field handles, otherwise temporary slaveMasterCoordinates is output
            alignOptimisation = None
            delta = None
            error = None
            alignObjective = None

            # restart element numbering to be above master
            maximumMasterElementId = zincutils.getMaximumElementId(masterMesh)
            zincutils.offsetElementIds(slaveMesh, maximumMasterElementId + slaveMesh.getSize())
            zincutils.renumberElementIds(slaveMesh, maximumMasterElementId + 1)
            # write elements to memory buffer
            sire = slaveRegion.createStreaminformationRegion()
            srme = sire.createStreamresourceMemory()
            if slaveMeshDimension == 3:
                domainTypes = Field.DOMAIN_TYPE_MESH3D
            elif slaveMeshDimension == 2:
                domainTypes = Field.DOMAIN_TYPE_MESH2D
            else:
                domainTypes = Field.DOMAIN_TYPE_MESH1D
            if slaveMeshDimension > 1:
                # destroy all slave faces so not merged into master
                slaveFaceMesh = slaveFm.findMeshByDimension(slaveMeshDimension - 1)
                slaveFaceMesh.destroyAllElements()
            sire.setResourceDomainTypes(srme, domainTypes)
            slaveRegion.write(sire)
            result, elementBuffer = srme.getBuffer()
            # destroy all elements and undefine coordinates in merged nodes then write nodes to memory buffer
            slaveMesh.destroyAllElements()
            nodetemplate_undefine_coordinates = slaveNodes.createNodetemplate()
            nodetemplate_undefine_coordinates.undefineField(slaveCoordinates)
            nodetemplate_undefine_coordinates.undefineField(slaveMasterCoordinates)
            for masterNodeId in self._mergeNodes:
                # using master numbering
                node = slaveNodes.findNodeByIdentifier(masterNodeId)
                node.merge(nodetemplate_undefine_coordinates)
                #slaveNodes.destroyNode(node)
            slaveMasterCoordinates = None

            sirn = slaveRegion.createStreaminformationRegion()
            srmn = sirn.createStreamresourceMemory()
            sirn.setResourceDomainTypes(srmn, Field.DOMAIN_TYPE_NODES)
            slaveRegion.write(sirn)
            result, nodeBuffer = srmn.getBuffer()
            slaveFm.endChange()
            masterFm.beginChange()
            sir1 = self._masterRegion.createStreaminformationRegion()
            srm1 = sir1.createStreamresourceMemoryBuffer(nodeBuffer)
            result = self._masterRegion.read(sir1)
            sir2 = self._masterRegion.createStreaminformationRegion()
            srm2 = sir2.createStreamresourceMemoryBuffer(elementBuffer)
            result = self._masterRegion.read(sir2)
            faceMesh = masterFm.findMeshByDimension(masterMeshDimension - 1)
            masterFm.defineAllFaces()
            masterFm.endChange()
            self._isMerged = True

            masterSlaveReferenceCoordinates = masterFm.findFieldByName(slaveReferenceCoordinatesName)

            if self.isFit() and (force or self.isPreviewFit()):
                QtGui.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
                # non-linear fit to original strains
                # make group of new slave nodes and elements for fitting
                slaveNodeGroup = masterFm.createFieldNodeGroup(masterNodes)
                slaveNodesetGroup = slaveNodeGroup.getNodesetGroup()
                slaveNodesetGroup.addNodesConditional(fieldTrue)
                slaveNodesetGroup.removeNodesConditional(origMasterNodeGroup)
                slaveElementGroup = masterFm.createFieldElementGroup(masterMesh)
                slaveMeshGroup = slaveElementGroup.getMeshGroup()
                slaveMeshGroup.addElementsConditional(fieldTrue)
                slaveMeshGroup.removeElementsConditional(origMasterElementGroup)

                offset = masterFm.createFieldConstant([0.0]*componentCount)
                print('offset', offset.getNumberOfComponents())
                offsetMasterCoordinates = masterFm.createFieldAdd(masterCoordinates, offset)
                conditionalOffsetMasterCoordinates = masterFm.createFieldIf(slaveNodeGroup, offsetMasterCoordinates, masterCoordinates)
                print('conditionalOffsetMasterCoordinates', conditionalOffsetMasterCoordinates.isValid(), conditionalOffsetMasterCoordinates.getNumberOfComponents())

                E2 = zincutils.getStrainField(masterCoordinates, masterSlaveReferenceCoordinates, masterMesh)
                #E2 = zincutils.getStrainField(conditionalOffsetMasterCoordinates, masterSlaveReferenceCoordinates, masterMesh)
                print('E2', E2.isValid())
                element = slaveMeshGroup.createElementiterator().next()
                xi = [0.5, 0.5, 0.5]
                result = masterCache.setMeshLocation(element, xi)
                result, values = masterSlaveReferenceCoordinates.evaluateReal(masterCache, componentCount)
                print('masterSlaveReferenceCoordinates ', result, values)
                result, values = masterCoordinates.evaluateReal(masterCache, componentCount)
                print('masterCoordinates ', result, values)
                result, values = offsetMasterCoordinates.evaluateReal(masterCache, componentCount)
                print('offsetMasterCoordinates ', result, values)
                result, values = conditionalOffsetMasterCoordinates.evaluateReal(masterCache, componentCount)
                print('conditionalOffsetMasterCoordinates ', result, values)
                diffOp = masterMesh.getChartDifferentialoperator(1, 1)
                result, values = conditionalOffsetMasterCoordinates.evaluateDerivative(diffOp, masterCache, componentCount)
                print('conditionalOffsetMasterCoordinates derivative ', result, values)
                result, values = E2.evaluateReal(masterCache, slaveMeshDimension*slaveMeshDimension)
                print('E2 ', result, values)

                #fieldassignment = masterCoordinates.createFieldassignment(

                strainObjective = masterFm.createFieldMeshIntegralSquares(E2, masterSlaveReferenceCoordinates, slaveMeshGroup)
                result = strainObjective.setNumbersOfPoints([4])
                #print('strainObjective.setNumbersOfPoints', result, 'components', strainObjective.getNumberOfComponents(), ' mesh size', slaveMeshGroup.getSize())
                #print('nodeset size', slaveNodesetGroup.getSize())

                fitOptimisation = masterFm.createOptimisation()
                fitOptimisation.setMethod(Optimisation.METHOD_LEAST_SQUARES_QUASI_NEWTON)  # AAA
                #fitOptimisation.setMethod(Optimisation.METHOD_QUASI_NEWTON)  # BBB
                fitOptimisation.setAttributeInteger(Optimisation.ATTRIBUTE_MAXIMUM_ITERATIONS, 10)
                fitOptimisation.setAttributeInteger(Optimisation.ATTRIBUTE_MAXIMUM_FUNCTION_EVALUATIONS, 1000)
                fitOptimisation.setAttributeReal(Optimisation.ATTRIBUTE_FUNCTION_TOLERANCE, 1.0e-8)  # 1.0e-8
                fitOptimisation.addObjectiveField(strainObjective)
                fitOptimisation.addIndependentField(masterCoordinates)  # AAA
                fitOptimisation.setConditionalField(masterCoordinates, slaveNodeGroup)
                #fitOptimisation.addIndependentField(offset)  # BBB

                result, fitObjectiveBefore = strainObjective.evaluateReal(masterCache, componentCount*componentCount)
                print(result, 'fitObjectiveBefore', fitObjectiveBefore)

                result = fitOptimisation.optimise()
                print('fitOptimisation result =', result)
                report = fitOptimisation.getSolutionReport()
                print(report)

                result, fitObjectiveAfter = strainObjective.evaluateReal(masterCache, componentCount*componentCount)
                print(result, 'fitObjectiveAfter', fitObjectiveAfter)

                QtGui.QApplication.restoreOverrideCursor()
                self._isFitted = True  # temporary

            # don't want masterSlaveReferenceCoordinates in output file:
            elementtemplate_undefine_coordinates = masterMesh.createElementtemplate()
            elementtemplate_undefine_coordinates.undefineField(masterSlaveReferenceCoordinates)
            elementiter = masterMesh.createElementiterator()
            element = elementiter.next()
            while element.isValid():
                element.merge(elementtemplate_undefine_coordinates)
                element = elementiter.next()
            nodetemplate_undefine_coordinates = masterNodes.createNodetemplate()
            nodetemplate_undefine_coordinates.undefineField(masterSlaveReferenceCoordinates)
            nodeiter = masterNodes.createNodeiterator()
            node = nodeiter.next()
            while node.isValid():
                node.merge(nodetemplate_undefine_coordinates)
                node = nodeiter.next()
            masterSlaveReferenceCoordinates.setManaged(False)
            masterSlaveReferenceCoordinates = None

        self._createGraphics(self._masterRegion)
        if self._sceneChangeCallback is not None:
            self._sceneChangeCallback()

    def _createGraphics(self, region):
        fm = region.getFieldmodule()
        meshDimension = self.getMeshDimension(region)
        coordinates = fm.findFieldByName('coordinates')
        nodeDerivativeFields = [
            fm.createFieldNodeValue(coordinates, Node.VALUE_LABEL_D_DS1, 1),
            fm.createFieldNodeValue(coordinates, Node.VALUE_LABEL_D_DS2, 1),
            fm.createFieldNodeValue(coordinates, Node.VALUE_LABEL_D_DS3, 1)
        ]
        elementDerivativeFields = []
        for d in range(meshDimension):
            elementDerivativeFields.append(fm.createFieldDerivative(coordinates, d + 1))
        elementDerivativesField = fm.createFieldConcatenate(elementDerivativeFields)
        cmiss_number = fm.findFieldByName('cmiss_number')
        # make graphics
        scene = region.getScene()
        scene.beginChange()
        axes = scene.createGraphicsPoints()
        pointattr = axes.getGraphicspointattributes()
        pointattr.setGlyphShapeType(Glyph.SHAPE_TYPE_AXES_XYZ)
        pointattr.setBaseSize([1.0,1.0,1.0])
        axes.setMaterial(self._materialmodule.findMaterialByName('grey50'))
        axes.setName('displayAxes')
        axes.setVisibilityFlag(self.isDisplayAxes())
        lines = scene.createGraphicsLines()
        lines.setCoordinateField(coordinates)
        lines.setName('displayLines')
        lines.setVisibilityFlag(self.isDisplayLines())
        nodeNumbers = scene.createGraphicsPoints()
        nodeNumbers.setFieldDomainType(Field.DOMAIN_TYPE_NODES)
        nodeNumbers.setCoordinateField(coordinates)
        pointattr = nodeNumbers.getGraphicspointattributes()
        pointattr.setLabelField(cmiss_number)
        pointattr.setGlyphShapeType(Glyph.SHAPE_TYPE_POINT)
        nodeNumbers.setMaterial(self._materialmodule.findMaterialByName('green'))
        nodeNumbers.setName('displayNodeNumbers')
        nodeNumbers.setVisibilityFlag(self.isDisplayNodeNumbers())
        elementNumbers = scene.createGraphicsPoints()
        elementNumbers.setFieldDomainType(Field.DOMAIN_TYPE_MESH_HIGHEST_DIMENSION)
        elementNumbers.setCoordinateField(coordinates)
        pointattr = elementNumbers.getGraphicspointattributes()
        pointattr.setLabelField(cmiss_number)
        pointattr.setGlyphShapeType(Glyph.SHAPE_TYPE_NONE)
        elementNumbers.setMaterial(self._materialmodule.findMaterialByName('cyan'))
        elementNumbers.setName('displayElementNumbers')
        elementNumbers.setVisibilityFlag(self.isDisplayElementNumbers())
        surfaces = scene.createGraphicsSurfaces()
        surfaces.setCoordinateField(coordinates)
        surfaces.setRenderPolygonMode(Graphics.RENDER_POLYGON_MODE_WIREFRAME if self.isDisplaySurfacesWireframe() else Graphics.RENDER_POLYGON_MODE_SHADED)
        surfaces.setExterior(self.isDisplaySurfacesExterior() if (meshDimension == 3) else False)
        surfacesMaterial = self._materialmodule.findMaterialByName('trans_blue' if self.isDisplaySurfacesTranslucent() else 'solid_blue')
        surfaces.setMaterial(surfacesMaterial)
        surfaces.setName('displaySurfaces')
        surfaces.setVisibilityFlag(self.isDisplaySurfaces())
        width = 0.02
        nodeDerivativeMaterialNames = [ 'gold', 'silver', 'green' ]
        for i in range(meshDimension):
            nodeDerivatives = scene.createGraphicsPoints()
            nodeDerivatives.setFieldDomainType(Field.DOMAIN_TYPE_NODES)
            nodeDerivatives.setCoordinateField(coordinates)
            pointattr = nodeDerivatives.getGraphicspointattributes()
            pointattr.setGlyphShapeType(Glyph.SHAPE_TYPE_ARROW_SOLID)
            pointattr.setOrientationScaleField(nodeDerivativeFields[i])
            pointattr.setBaseSize([0.0, width, width])
            pointattr.setScaleFactors([1.0, 0.0, 0.0])
            nodeDerivatives.setMaterial(self._materialmodule.findMaterialByName(nodeDerivativeMaterialNames[i]))
            nodeDerivatives.setName('displayNodeDerivatives')
            nodeDerivatives.setVisibilityFlag(self.isDisplayNodeDerivatives())

        xiAxes = scene.createGraphicsPoints()
        xiAxes.setFieldDomainType(Field.DOMAIN_TYPE_MESH_HIGHEST_DIMENSION)
        xiAxes.setCoordinateField(coordinates)
        pointattr = xiAxes.getGraphicspointattributes()
        pointattr.setGlyphShapeType(Glyph.SHAPE_TYPE_AXES_123)
        pointattr.setOrientationScaleField(elementDerivativesField)
        if meshDimension == 1:
            pointattr.setBaseSize([0.0, 2*width, 2*width])
            pointattr.setScaleFactors([0.25, 0.0, 0.0])
        elif meshDimension == 2:
            pointattr.setBaseSize([0.0, 0.0, 2*width])
            pointattr.setScaleFactors([0.25, 0.25, 0.0])
        else:
            pointattr.setBaseSize([0.0, 0.0, 0.0])
            pointattr.setScaleFactors([0.25, 0.25, 0.25])
        xiAxes.setMaterial(self._materialmodule.findMaterialByName('yellow'))
        xiAxes.setName('displayXiAxes')
        xiAxes.setVisibilityFlag(self.isDisplayXiAxes())

        scene.endChange()

    def getOutputModelFilename(self):
        return self._filenameStem + '.ex2'

    def _writeModel(self):
        if not (self._isMerged and self._isFitted):
            self._mergeMesh(force = True)
        self._masterRegion.writeFile(self.getOutputModelFilename())

    def done(self):
        self._saveSettings()
        self._writeModel()
