'''
Created on Sep 10, 2017

@author: Richard Christie
'''

import os, sys
import json

from opencmiss.zinc.context import Context
from opencmiss.zinc.result import RESULT_OK
from opencmiss.zinc.field import Field
from opencmiss.zinc.glyph import Glyph
from opencmiss.zinc.material import Material
from opencmiss.zinc.node import Node
from opencmiss.zinc.optimisation import Optimisation
from mapclientplugins.meshmergerstep.utils import zinc as zincutils

STRING_FLOAT_FORMAT = '{:.8g}'

class MeshMergerModel(object):
    '''
    Framework for generating meshes of a number of types, with mesh type specific options
    '''

    def __init__(self, location, identifier, masterFilename, slaveFilename):
        '''
        Constructor
        '''
        self._location = location
        self._identifier = identifier
        self._filenameStem = os.path.join(self._location, self._identifier)
        self._context = Context("MeshMerger")
        self._masterRegion = self._context.createRegion()
        self._slaveRegion = self._context.createRegion()
        self._masterFilename = masterFilename
        self._slaveFilename = slaveFilename
        tess = self._context.getTessellationmodule().getDefaultTessellation()
        tess.setRefinementFactors(12)
        self._sceneChangeCallback = None
        # set up standard materials and glyphs so we can use them elsewhere
        self._materialmodule = self._context.getMaterialmodule()
        self._materialmodule.defineStandardMaterials()
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
        self._mergeNodes = []
        self._settings = {
            'mergeNodes' : '',
            'previewAlign' : True,
            'previewFit' : False,
            'displayAxes' : True,
            'displayElementNumbers' : True,
            'displayLines' : True,
            'displayNodeDerivatives' : False,
            'displayNodeNumbers' : True,
            'displaySurfaces' : True,
            'displayXiAxes' : False
        }
        self._loadSettings()
        self._slaveRegion.readFile(self._slaveFilename)
        self._createGraphics(self._slaveRegion)
        if self._settings['previewAlign'] and (len(self._mergeNodes) > 0):
            # _mergeMesh reads the master mesh and creates graphics
            self._mergeMesh()
        else:
            self._masterRegion.readFile(self._masterFilename)
            self._createGraphics(self._masterRegion)

    def getMergeNodesText(self):
        return self._settings['mergeNodes']

    def checkMasterNodeId(self, masterNodeId):
        masterNodes = self._masterRegion.getFieldmodule().findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
        masterNode = masterNodes.findNodeByIdentifier(masterNodeId)
        return masterNode.isValid()

    def checkSlaveNodeId(self, slaveNodeId):
        slaveNodes = self._slaveRegion.getFieldmodule().findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
        slaveNode = slaveNodes.findNodeByIdentifier(slaveNodeId)
        return slaveNode.isValid()

    def findMergeSlaveNodeId(self, masterNodeId):
        for mergeNodesPair in self._mergeNodes:
            if mergeNodesPair[0] == masterNodeId:
                return mergeNodesPair[1]
        return -1

    def _makeMergeNodesText(self):
        mergeNodesText = ''
        for mergeNodesPair in self._mergeNodes:
            mergeNodesText += str(mergeNodesPair[0]) + '=' + str(mergeNodesPair[1]) + '\n'
        self._settings['mergeNodes'] = mergeNodesText

    def _parseMergeNodesText(self, mergeNodesText):
        self._mergeNodes = []
        for mergeNodesText in mergeNodesText.split():
            try:
                ends = mergeNodesText.split('=')
                self._mergeNodes.append((int(ends[0]), int(ends[1])))
            except:
                pass
        self._makeMergeNodesText()

    def mergeNodes(self, masterNodeId, slaveNodeId):
        if not (self.checkMasterNodeId(masterNodeId) and self.checkSlaveNodeId(slaveNodeId)):
            return false
        found = False
        index = 0
        for mergeNodesPair in self._mergeNodes:
            if mergeNodesPair[0] == masterNodeId:
                if mergeNodesPair[1] == slaveNodeId:
                    return False
                self._mergeNodes[index] = (masterNodeId, slaveNodeId)
                found = True
                break
            elif mergeNodesPair[0] > masterNodeId:
                self._mergeNodes.insert(index, (masterNodeId, slaveNodeId))
                found = True
                break
            index += 1
        if not found:
            self._mergeNodes.append((masterNodeId, slaveNodeId))
        self._makeMergeNodesText()
        if self.isPreviewAlign():
            self._mergeMesh()
        return True

    def deleteMergeNode(self, masterNodeId):
        for mergeNodesPair in self._mergeNodes:
            if mergeNodesPair[0] == masterNodeId:
                self._mergeNodes.remove(mergeNodesPair)
                self._makeMergeNodesText()
                if self.isPreviewAlign():
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
        except:
            pass  # no settings saved yet

    def _saveSettings(self):
        with open(self._filenameStem + '-settings.json', 'w') as f:
            f.write(json.dumps(self._settings, default=lambda o: o.__dict__, sort_keys=True, indent=4))

    def isPreviewAlign(self):
        return self._settings['previewAlign']

    def setPreviewAlign(self, preview):
        self._settings['previewAlign'] = preview
        if self.isPreviewAlign():
            self._mergeMesh()

    def isPreviewFit(self):
        return self._settings['previewFit']

    def setPreviewFit(self, fit):
        self._settings['previewFit'] = fit
        if self.isPreviewAlign() and self.isPreviewFit():
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

    def isDisplayXiAxes(self):
        return self._getVisibility('displayXiAxes')

    def setDisplayXiAxes(self, show):
        self._setVisibility('displayXiAxes', show)

    def _mergeMesh(self):
        self._masterRegion = self._context.createRegion()
        self._masterRegion.readFile(self._masterFilename)
        if len(self._mergeNodes) > 0:
            # perform merge of slave into master
            masterFm = self._masterRegion.getFieldmodule()
            masterNodes = masterFm.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
            maximumMasterNodeId = zincutils.getMaximumNodeId(masterNodes)
            masterCoordinates = masterFm.findFieldByName('coordinates').castFiniteElement()
            masterCache = masterFm.createFieldcache()
            for dimension in range(3,0,-1):
                masterMesh = masterFm.findMeshByDimension(dimension)
                if masterMesh.getSize() > 0:
                    break
            masterMeshDimension = masterMesh.getDimension()
            # modify copy of slave region
            slaveRegion = self._context.createRegion()
            slaveRegion.readFile(self._slaveFilename)
            slaveFm = slaveRegion.getFieldmodule()
            slaveNodes = slaveFm.findNodesetByFieldDomainType(Field.DOMAIN_TYPE_NODES)
            maximumSlaveNodeId = zincutils.getMaximumNodeId(slaveNodes)
            slaveCoordinates = slaveFm.findFieldByName('coordinates').castFiniteElement()
            # note: can't handle mix of component counts
            componentCount = slaveCoordinates.getNumberOfComponents()
            slaveCache = slaveFm.createFieldcache()
            for dimension in range(3,0,-1):
                slaveMesh = slaveFm.findMeshByDimension(dimension)
                if slaveMesh.getSize() > 0:
                    break
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
            for mergeNodesPair in self._mergeNodes:
                masterNode = masterNodes.findNodeByIdentifier(mergeNodesPair[0])
                masterCache.setNode(masterNode)
                result, masterX = masterCoordinates.evaluateReal(masterCache, componentCount)
                #print('master ',mergeNodesPair[0],'result',result,masterX)
                slaveNode = slaveNodes.findNodeByIdentifier(mergeNodesPair[1])
                slaveNode.merge(nodetemplate)
                slaveMatchedNodesGroup.addNode(slaveNode)
                slaveCache.setNode(slaveNode)
                result, slaveX = slaveCoordinates.evaluateReal(slaveCache, componentCount)
                #print(' slave ',mergeNodesPair[1],'result',result,slaveX)
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
                for mergeNodesPair in self._mergeNodes:
                    if oldId == (mergeNodesPair[1] + idOffset):
                        newId = mergeNodesPair[0]
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
            print('rotatedSlaveCoordinates.isValid() =',rotatedSlaveCoordinates.isValid())
            delta = slaveFm.createFieldSubtract(rotatedSlaveCoordinates, slaveMasterCoordinates)
            error = slaveFm.createFieldMagnitude(delta)
            objective = slaveFm.createFieldNodesetSum(error, slaveMatchedNodesGroup)
            print('objective.isValid() =', objective.isValid(), '#nodes=', slaveMatchedNodesGroup.getSize())
            #result, matrixBefore = rotationMatrix.evaluateReal(slaveCache, 9)
            #print(result, 'matrixBefore', matrixBefore)
            result, objectiveBefore = objective.evaluateReal(slaveCache, 1)
            print(result, 'objectiveBefore', objectiveBefore)
            eulerAngles = slaveFm.createFieldConcatenate([azimuth, elevation, roll])
            result, eulerAnglesBefore = eulerAngles.evaluateReal(slaveCache, 3)
            print(result, 'eulerAnglesBefore', eulerAnglesBefore)

            optimisation = slaveFm.createOptimisation()
            optimisation.setMethod(Optimisation.METHOD_QUASI_NEWTON)
            optimisation.setAttributeInteger(Optimisation.ATTRIBUTE_MAXIMUM_ITERATIONS, 100)
            optimisation.setAttributeInteger(Optimisation.ATTRIBUTE_MAXIMUM_FUNCTION_EVALUATIONS, 1000)
            optimisation.setAttributeReal(Optimisation.ATTRIBUTE_FUNCTION_TOLERANCE, 1.0e-8)  # 1.0e-8
            optimisation.addObjectiveField(objective)
            optimisation.addIndependentField(azimuth)
            optimisation.addIndependentField(elevation)
            optimisation.addIndependentField(roll)

            result = optimisation.optimise()
            #print('optimisation result =', result)
            #report = optimisation.getSolutionReport()
            #print(report)

            result, matrixAfter = rotationMatrix.evaluateReal(slaveCache, 9)
            #print(result, 'matrixAfter', matrixAfter)
            result, objectiveAfter = objective.evaluateReal(slaveCache, 1)
            print(result, 'objectiveAfter', objectiveAfter)
            result, eulerAnglesAfter = eulerAngles.evaluateReal(slaveCache, 3)
            print(result, 'eulerAnglesAfter', eulerAnglesAfter)

            zincutils.transformNodeCoordinates(slaveNodes, slaveCoordinates, matrixAfter, masterMeanX)

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
            # destroy all elements and merged nodes then write nodes to memory buffer
            slaveMesh.destroyAllElements()
            for mergeNodesPair in self._mergeNodes:
                # using master numbering
                node = slaveNodes.findNodeByIdentifier(mergeNodesPair[0])
                slaveNodes.destroyNode(node)
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
        self._createGraphics(self._masterRegion)
        if self._sceneChangeCallback is not None:
            self._sceneChangeCallback()

    def _createGraphics(self, region):
        fm = region.getFieldmodule()
        for dimension in range(3,0,-1):
            mesh = fm.findMeshByDimension(dimension)
            if mesh.getSize() > 0:
                break
        meshDimension = mesh.getDimension()
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
        pointattr.setGlyphShapeType(Glyph.SHAPE_TYPE_NONE)
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
        if meshDimension == 3:
            surfaces.setExterior(True)
        surfaces.setMaterial(self._materialmodule.findMaterialByName('trans_blue'))
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
        self._masterRegion.writeFile(self.getOutputModelFilename())

    def done(self):
        self._saveSettings()
        self._writeModel()
