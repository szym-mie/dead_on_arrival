from src.resource.resource_manager import ResourceManager

conf_pack = ResourceManager('./conf', './pack/pack_conf.json')
base_pack = ResourceManager('./res', './pack/pack_base.json')


def reload_base():
    base_pack.reload_pack()


def reload_conf():
    conf_pack.reload_pack()


def load_all():
    reload_conf()
    reload_base()
