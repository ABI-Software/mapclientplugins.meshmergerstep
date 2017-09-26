'''
Created on Sept 27, 2017

@author: Richard Christie
'''
from opencmiss.zinc.node import Node
from opencmiss.zinc.result import RESULT_OK, RESULT_WARNING_PART_DONE

def createRotationMatrixField(azimuth, elevation, roll):
    """
    Create 3x3 rotation matrix field from scalar azimuth, elevation and roll Euler angle fields
    """
    fm = azimuth.getFieldmodule()
    fm.beginChange()
    minus_one = fm.createFieldConstant([-1.0])
    cos_azimuth = fm.createFieldCos(azimuth)
    sin_azimuth = fm.createFieldSin(azimuth)
    cos_elevation = fm.createFieldCos(elevation)
    sin_elevation = fm.createFieldSin(elevation)
    cos_roll = fm.createFieldCos(roll)
    sin_roll = fm.createFieldSin(roll)
    cos_azimuth_sin_elevation = fm.createFieldMultiply(cos_azimuth, sin_elevation)
    sin_azimuth_sin_elevation = fm.createFieldMultiply(sin_azimuth, sin_elevation)
    # matrix[0][0] = cos_azimuth*cos_elevation;
    m11 = fm.createFieldMultiply(cos_azimuth, cos_elevation)
    # matrix[0][1] = sin_azimuth*cos_elevation;
    m12 = fm.createFieldMultiply(sin_azimuth, cos_elevation)
    # matrix[0][2] = -sin_elevation;
    m13 = fm.createFieldMultiply(minus_one, sin_elevation)
    # matrix[1][0] = cos_azimuth*sin_elevation*sin_roll - sin_azimuth*cos_roll;
    m21a = fm.createFieldMultiply(cos_azimuth_sin_elevation, sin_roll)
    m21b = fm.createFieldMultiply(sin_azimuth, cos_roll)
    m21 = fm.createFieldSubtract(m21a, m21b)
    # matrix[1][1] = sin_azimuth*sin_elevation*sin_roll + cos_azimuth*cos_roll;
    m22a = fm.createFieldMultiply(sin_azimuth_sin_elevation, sin_roll)
    m22b = fm.createFieldMultiply(cos_azimuth, cos_roll)
    m22 = fm.createFieldAdd(m22a, m22b)
    # matrix[1][2] = cos_elevation*sin_roll;
    m23 = fm.createFieldMultiply(cos_elevation, sin_roll)
    # matrix[2][0] = cos_azimuth*sin_elevation*cos_roll + sin_azimuth*sin_roll;
    m31a = fm.createFieldMultiply(cos_azimuth_sin_elevation, cos_roll)
    m31b = fm.createFieldMultiply(sin_azimuth, sin_roll)
    m31 = fm.createFieldAdd(m31a, m31b)
    # matrix[2][1] = sin_azimuth*sin_elevation*cos_roll - cos_azimuth*sin_roll;
    m32a = fm.createFieldMultiply(sin_azimuth_sin_elevation, cos_roll)
    m32b = fm.createFieldMultiply(cos_azimuth, sin_roll)
    m32 = fm.createFieldSubtract(m32a, m32b)
    # matrix[2][2] = cos_elevation*cos_roll;
    m33 = fm.createFieldMultiply(cos_elevation, cos_roll)
    rotationMatrix = fm.createFieldConcatenate([m11, m12, m13, m21, m22, m23, m31, m32, m33])
    fm.endChange()
    return rotationMatrix


def getMaximumNodeId(nodeset):
    """
    :return: Maximum node identifier in nodeset or -1 if none.
    """
    maximumNodeId = -1
    nodeiterator = nodeset.createNodeiterator()
    node = nodeiterator.next()
    while node.isValid():
        id = node.getIdentifier()
        if id > maximumNodeId:
            maximumNodeId = id
        node = nodeiterator.next()
    return maximumNodeId


def offsetNodeIds(nodeset, idOffset):
    """
    Offset all node identifiers in nodeset by idOffset.
    Note up to caller to ensure no nodes are using the target ids.
    """
    fm = nodeset.getFieldmodule()
    fm.beginChange()
    idMaps = []
    nodeiterator = nodeset.createNodeiterator()
    node = nodeiterator.next()
    while node.isValid():
        id = node.getIdentifier()
        idMaps.append((id, id + idOffset))
        node = nodeiterator.next()
    for idMap in idMaps:
        node = nodeset.findNodeByIdentifier(idMap[0])
        node.setIdentifier(idMap[1])
    fm.endChange()


def getMaximumElementId(mesh):
    """
    :return: Maximum element identifier in mesh or -1 if none.
    """
    maximumElementId = -1
    elementiterator = mesh.createElementiterator()
    element = elementiterator.next()
    while element.isValid():
        id = element.getIdentifier()
        if id > maximumElementId:
            maximumElementId = id
        element = elementiterator.next()
    return maximumElementId


def offsetElementIds(mesh, idOffset):
    """
    Offset all element identifiers in mesh by idOffset.
    Note up to caller to ensure no elements are using the target ids.
    """
    fm = mesh.getFieldmodule()
    fm.beginChange()
    idMaps = []
    elementiterator = mesh.createElementiterator()
    element = elementiterator.next()
    while element.isValid():
        id = element.getIdentifier()
        idMaps.append((id, id + idOffset))
        element = elementiterator.next()
    for idMap in idMaps:
        element = mesh.findElementByIdentifier(idMap[0])
        element.setIdentifier(idMap[1])
    fm.endChange()


def renumberElementIds(mesh, firstId):
    """
    Renumber elements in mesh consecutively from firstId
    """
    fm = mesh.getFieldmodule()
    fm.beginChange()
    idMaps = []
    nextId = firstId
    elementiterator = mesh.createElementiterator()
    element = elementiterator.next()
    while element.isValid():
        id = element.getIdentifier()
        idMaps.append((id, nextId))
        nextId += 1
        element = elementiterator.next()
    for idMap in idMaps:
        element = mesh.findElementByIdentifier(idMap[0])
        element.setIdentifier(idMap[1])
    fm.endChange()


def translateNodeCoordinates(nodeset, field, offset):
    """
    Translate node coordinates. Does not handle versions yet.
    :fm: Fieldmodule which nodeset and coordinates belong to
    :nodeset: Set of nodes to transform coordinates of
    :field: Zinc finite element field giving coordinates.
    :offset: offset to add to coordinates
    """
    fm = field.getFieldmodule()
    fm.beginChange()
    cache = fm.createFieldcache()
    nodeiterator = nodeset.createNodeiterator()
    node = nodeiterator.next()
    componentCount = field.getNumberOfComponents()
    while node.isValid():
        cache.setNode(node)
        result, x = field.evaluateReal(cache, 3)
        for c in range(componentCount):
            x[c] += offset[c]
        result = field.assignReal(cache, x)
        node = nodeiterator.next()
    fm.endChange()


def transformNodeCoordinates(nodeset, field, rotationScale, offset, time = 0.0):
    '''
    Transform node coordinates by matrix and offset, handling node derivatives and versions.
    Only works for rectangular cartesian coordinates
    :param nodeset: the set of nodes to transform
    :param field: the coordinate field of finite element type, up to 3 components
    :param rotationScale: 3x3 pre-multiply rotation scale matrix as a list of 9 values,
        cycling across rows fastest.
    :param offset: list containing coordinates offset
    '''
    componentCount = field.getNumberOfComponents()
    if componentCount > 3:
        print('zinc.transformNodeCoordinates: Coordinate field has more than 3 components')
        raise
    if len(rotationScale) != 9:
        print('zinc.transformNodeCoordinates: rotationScale does not have 9 components (3x3 matrix)')
        raise
    success = True
    fm = field.getFieldmodule()
    fm.beginChange()
    cache = fm.createFieldcache()
    cache.setTime(time)
    nodetemplate = nodeset.createNodetemplate()
    valueLabels = [Node.VALUE_LABEL_VALUE, Node.VALUE_LABEL_D_DS1, Node.VALUE_LABEL_D_DS2, Node.VALUE_LABEL_D2_DS1DS2,
        Node.VALUE_LABEL_D_DS3, Node.VALUE_LABEL_D2_DS1DS3, Node.VALUE_LABEL_D2_DS2DS3, Node.VALUE_LABEL_D3_DS1DS2DS3]
    nodeIter = nodeset.createNodeiterator()
    node = nodeIter.next()
    while node.isValid():
        nodetemplate.defineFieldFromNode(field, node)
        cache.setNode(node)
        for valueLabel in valueLabels:
            versionsCount = nodetemplate.getValueNumberOfVersions(field, -1, valueLabel)
            for v in range(versionsCount):
                result, x = field.getNodeParameters(cache, -1, valueLabel, v + 1, componentCount)
                if (result == RESULT_OK) or (result == RESULT_WARNING_PART_DONE):
                    newx = [0.0]*componentCount
                    for c in range(componentCount):
                        if valueLabel == Node.VALUE_LABEL_VALUE:
                            newx[c] = offset[c]
                        for d in range(componentCount):
                            newx[c] += rotationScale[c*3 + d]*x[d]
                    result = field.setNodeParameters(cache, -1, valueLabel, v + 1, newx)
                    if (result != RESULT_OK) and (result != RESULT_WARNING_PART_DONE):
                        success = False
                elif result != RESULT_ERROR_NOT_FOUND:
                    success = False
        node = nodeIter.next()
    fm.endChange()
    if not success:
        print('zinc.transformNodeCoordinates: failed to get/set some values')
        raise
