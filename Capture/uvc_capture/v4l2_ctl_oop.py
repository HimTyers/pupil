from v4l2_ctl import *

class Control(dict):
    """
    docstring
    """
    def __init__(self,c):
        for key,val in c.items():
            self[key] = val

        self.name = self['name']
        self.atb_name = self['name']
        self.order = self['order']
        self.value = self['value']
        self.default = self['default']
        self.type  = self['type']
        if self.type == 'menu':
            self.menu = self['menu']
            self.min = None
            self.max = None
            self.step = None
        elif self.type == 'bool':
            self.min = 0
            self.max = 1
            self.step = 1
            self.menu=None
        else:
            self.menu=None
            self.step = self['step']
            self.min = self['min']
            self.max = self['max']
        
        if 'flags' in self:
            self.flags = self['flags']
        else:
            self.flags = "active"


    def get_val(self):
        return self['value']

    def set_val(self,val):
        set(self['src'],self['name'],val)
        self['value'] = val


class Camera(object):
    """docstring for uvcc_camera"""
    def __init__(self,c):
        self.dict = c
        self.cv_id = c['src_id']
        self.name = c['name']
        self.manufacurer = None
        self.serial = c['serial']

    def init_controls(self):
        control_dict = extract_controls(self.cv_id)

        self.controls = {}
        for c in control_dict:
            self.controls[c] = Control(control_dict[c])

    def load_defaults(self):
        for c in self.controls.itervalues():
            c.set_val(c.default)

    def update_from_device(self):
        update_from_device(self.controls)

class Camera_List(list):
    """docstring for Camera_List"""

    def __init__(self):
        for c in list_devices():
            self.append(Camera(c))


    def release(self):
        """
        call when done with class instance
        """
        pass



if __name__ == '__main__':
    uvc_cameras = Camera_List()
    for cam in uvc_cameras:
        print cam.name
        cam.init_controls()
        cam.load_defaults()
        cam.update_from_device()
        for c in cam.controls.itervalues():
            if c.flags == "active":
                print c.name, " "*(40-len(c.name)), c.current,c.type, c.min,c.max,c.step
    uvc_cameras.release()
