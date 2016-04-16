import unittest
from central.central import Central as sut

class DeviceMock():
    def doStuff(self):
        return "Doing Stuff"
    def doExceptionalStuff(self, exceptionType):
        raise exceptionType

    def doStuffWithArgs(self, **kwargs):
        return kwargs

class SanityTests(unittest.TestCase):
    def setUp(self):
        self.haus= sut()
        self.devName='devMock'

    def test_canIEvenDoAnObject(self):
        self.assertNotEqual(self.haus, None)

    def test_sanitySelfCheck(self):
        self.assertIsNotNone(self.haus['self'][1])

class DevicesManagementTests(unittest.TestCase):
    def setUp(self):
        self.haus= sut()
        self.devName='devMock'
        self.haus.addDevice(DeviceMock, self.devName)

    def assertResultIsError(self, resultToCheck):
        self.assertIn('error',resultToCheck['result'])

    def assertDeviceNotOnList(self, deviceName):
        self.assertFalse((deviceName in self.haus.getAllDevices()[1]))

    def assertDeviceOnList(self, deviceName):
        self.assertTrue((deviceName in self.haus.getAllDevices()[1]))

    def test_addDeviceNewStyle(self):
        newStyle= 'newDevice'
        self.haus[newStyle]=(DeviceMock, None)
        self.assertDeviceOnList(newStyle)

    def test_RemoveInvalidDeviceNewStyle(self):
        self.assertRaises(KeyError, self.haus.removeDevice, 'selfie')

    def test_inspectInvalidDeviceNewStyle(self):
        self.assertRaises(KeyError, self.haus.__getitem__, 'selfie')
        self.assertRaises(KeyError, lambda: self.haus['selfie'])

    def test_inspectDeviceNewStyle(self):
        result= self.haus['self']
        self.assertEquals('ok',result[0])

    def test_howManyDevices(self):
        count= len(self.haus._devices)
        self.assertEquals(count, len(self.haus))

    def test_addStaticDevice(self):
        self.assertDeviceOnList(self.devName)

    def test_addDeviceFromDynamicSource(self):
        self.haus.addDevice('dynamicClass','dynamicClassDevice', 'dynamic')
        self.assertDeviceOnList(self.devName)

    def test_addTwoDevsWithSameName(self):
        self.assertRaises(KeyError, self.haus.addDevice,DeviceMock, self.devName)

    def test_removeDevice(self):
        self.haus.removeDevice(self.devName)
        self.assertDeviceNotOnList(self.devName)

    def test_removeDeviceSelfReturnResultErrorAndDeviceIsNotRemoved(self):
        self.assertRaises(KeyError, self.haus.removeDevice, 'self')
        self.assertDeviceOnList('self')

    def test_iterateOverDevices(self):
        result=[]
        for dev in self.haus:
            result.append(dev)
        self.assertIn('self', result)
        self.assertIn(self.devName, result)

    def test_performedActionThrowsExceptionExpectDetails(self):
        exceptionInfo='Mock SysError'
        results= self.haus.action(self.devName, 'doExceptionalStuff',SystemError(exceptionInfo))
        self.assertIn('error',results['result'])
        self.assertIn(exceptionInfo, results['details'])

    def test_removeDeviceWithInterface(self):
        self.assertIn(self.devName , self.haus.getAllDevices()[1])
        self.haus.action('self', 'removeDevice', device= self.devName)
        self.assertNotIn(self.devName , self.haus.getAllDevices()[1])

    def test_addDeviceWithInterfaceAndRemoveItWithoutNamedParameters(self):
        self.haus.action('self', 'addDevice', DeviceMock, self.devName)
        self.assertIn(self.devName , self.haus.getAllDevices()[1])
        self.haus.action('self', 'removeDevice', self.devName)
        self.assertNotIn(self.devName , self.haus.getAllDevices()[1])

    def test_inspectOnDevice(self):
        self.assertIn('doStuff',self.haus[self.devName][1])

    def test_performActionOnSelfByInterface(self):
        self.assertIn('self', self.haus.action('self', 'getAllDevices')['details'])

    def test_performActionOnDevice(self):
        commandResult= self.haus.action(self.devName,'doStuff')
        self.assertEqual(commandResult['result'], 'ok')

    def test_performActionWithArgumentsOnDevice(self):
        result= self.haus.action(self.devName, 'doStuffWithArgs', arg1=0, arg2='dwa')
        self.assertEquals({'arg1':0, 'arg2':'dwa'}, result['details'])

