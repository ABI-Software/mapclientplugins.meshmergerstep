
"""
MAP Client Plugin Step
"""
import json

from PySide6 import QtGui, QtWidgets

from mapclient.mountpoints.workflowstep import WorkflowStepMountPoint
from mapclientplugins.meshmergerstep.configuredialog import ConfigureDialog
from mapclientplugins.meshmergerstep.model.meshmergermodel import MeshMergerModel
from mapclientplugins.meshmergerstep.view.meshmergerwidget import MeshMergerWidget


class MeshMergerStep(WorkflowStepMountPoint):
    """
    Skeleton step which is intended to be a helpful starting point
    for new steps.
    """

    def __init__(self, location):
        super(MeshMergerStep, self).__init__('Mesh Merger', location)
        self._configured = False # A step cannot be executed until it has been configured.
        self._category = 'Fitting'
        # Add any other initialisation code here:
        self._icon =  QtGui.QImage(':/meshmergerstep/images/fitting.png')
        # Ports:
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#file_location'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#uses',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#file_location'))
        self.addPort(('http://physiomeproject.org/workflow/1.0/rdf-schema#port',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#provides',
                      'http://physiomeproject.org/workflow/1.0/rdf-schema#file_location'))
        # Port data:
        self._portData0 = None # http://physiomeproject.org/workflow/1.0/rdf-schema#file_location
        self._portData1 = None # http://physiomeproject.org/workflow/1.0/rdf-schema#file_location
        self._portData2 = None # http://physiomeproject.org/workflow/1.0/rdf-schema#file_location
        # Config:
        self._config = {}
        self._config['identifier'] = ''
        self._model = None
        self._view = None

    def execute(self):
        """
        Kick off the execution of the step, in this case an interactive dialog.
        User invokes the _doneExecution() method when finished, via pushbutton.
        """
        self._model = MeshMergerModel()
        try_again = True
        while try_again:
            try:
                self._model.configure(self._location, self._config['identifier'], self._portData0, self._portData1)
                try_again = False
            except Exception as e:
                result = QtWidgets.QMessageBox.warning(None, 'Mesh Merger Configuration Failure',
                    'Unexpected exception \'' + str(e) + '\'. Do you want to retry (recommended)?.',
                    QtWidgets.QMessageBox.Retry | QtWidgets.QMessageBox.Abort, QtWidgets.QMessageBox.Retry)
                if result == QtWidgets.QMessageBox.Abort:
                    raise
        self._view = MeshMergerWidget(self._model)
        self._view.registerDoneExecution(self._myDoneExecution)
        self._setCurrentWidget(self._view)

    def _myDoneExecution(self):
        self._portData2 = self._model.getOutputModelFilename()
        self._view = None
        self._model = None
        self._doneExecution()

    def setPortData(self, index, dataIn):
        """
        Add your code here that will set the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        uses port for this step then the index can be ignored.

        :param index: Index of the port to return.
        :param dataIn: The data to set for the port at the given index.
        """
        if index == 0:
            self._portData0 = dataIn # http://physiomeproject.org/workflow/1.0/rdf-schema#file_location
        elif index == 1:
            self._portData1 = dataIn # http://physiomeproject.org/workflow/1.0/rdf-schema#file_location

    def getPortData(self, index):
        """
        Add your code here that will return the appropriate objects for this step.
        The index is the index of the port in the port list.  If there is only one
        provides port for this step then the index can be ignored.

        :param index: Index of the port to return.
        """
        return self._portData2 # http://physiomeproject.org/workflow/1.0/rdf-schema#file_location

    def configure(self):
        """
        This function will be called when the configure icon on the step is
        clicked.  It is appropriate to display a configuration dialog at this
        time.  If the conditions for the configuration of this step are complete
        then set:
            self._configured = True
        """
        dlg = ConfigureDialog(QtWidgets.QApplication.activeWindow().current_widget())
        dlg.identifierOccursCount = self._identifierOccursCount
        dlg.setConfig(self._config)
        dlg.validate()
        dlg.setModal(True)

        if dlg.exec_():
            self._config = dlg.getConfig()

        self._configured = dlg.validate()
        self._configuredObserver()

    def getIdentifier(self):
        """
        The identifier is a string that must be unique within a workflow.
        """
        return self._config['identifier']

    def setIdentifier(self, identifier):
        """
        The framework will set the identifier for this step when it is loaded.
        """
        self._config['identifier'] = identifier

    def serialize(self):
        """
        Add code to serialize this step to string.  This method should
        implement the opposite of 'deserialize'.
        """
        return json.dumps(self._config, default=lambda o: o.__dict__, sort_keys=True, indent=4)

    def deserialize(self, string):
        """
        Add code to deserialize this step from string.  This method should
        implement the opposite of 'serialize'.

        :param string: JSON representation of the configuration in a string.
        """
        self._config.update(json.loads(string))

        d = ConfigureDialog()
        d.identifierOccursCount = self._identifierOccursCount
        d.setConfig(self._config)
        self._configured = d.validate()


