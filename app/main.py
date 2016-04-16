class Hauser:
    def __init__(self):
        self._devices={
                'self'   : self}
    def _listDevices(self):
        return [ device for device in self._devices.keys() ]

    def action(self, device, action, *args, **kwargs):
        try:
            if device == 'self': result, details= getattr(self._devices[device], action)(*args, **kwargs)
            else:
                result= 'ok'
                details= getattr(self._devices[device], action)(*args, **kwargs)
        except Exception as e:
            result= 'error'
            details= str(e)
        return { 'result': result, 'details': details}

    def addDevice(self, deviceClassName, internalName, fromWhatModule=None):
        if internalName in self._devices: return ('error', 'Key "%s" already in use' % internalName)
        if fromWhatModule: self._devices[internalName]= getattr(__import__(fromWhatModule), deviceClassName)
        else: self._devices[internalName]= deviceClassName()
        return self.getAllDevices()

    def removeDevice(self, internalName):
        if internalName == 'self': return ('error', 'Cannot remove "self" from devices')
        del self._devices[internalName]
        return self.getAllDevices()

    def inspect(self, device='self'):
        if device in self._devices:
            return ('ok', [cmd for cmd in dir(self._devices[device]) if not cmd.startswith('_')])
        else:
            return ('error', 'Device %s not installed' % device);

    def inspectAll(self):
        allDevices={}
        for device in self._devices:
            allDevices[device]=self.inspect(device)
        return ('ok', allDevices)

    def getAllDevices(self):
        return ('ok', self._listDevices())

