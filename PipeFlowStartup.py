import unreal

@unreal.uclass()
class LaunchToolWidget(unreal.ToolMenuEntryScript):
    def setToolPath(self, path):#"/Game/Y24/Tools/W_AssetImporter"
        self.toolPath = path

    @unreal.ufunction(override=True)
    def execute(self, context):
        #print("EXECUTE SCRIPT")
        unreal.EditorUtilitySubsystem().spawn_and_register_tab(unreal.EditorAssetLibrary.load_asset(self.toolPath))

#Generate New Menu
menus = unreal.ToolMenus.get()
main_menu = menus.find_menu("LevelEditor.MainMenu")
tools_menu = main_menu.add_sub_menu("Pipeflow", "PythonAutomation", "Pipeflow", "Pipeflow")
#Generate Asset Management section
tools_menu.add_section("AssetManagement", "Asset Management")
menus.refresh_all_widgets()

#Asset Importer Tool
assetImporterTool = LaunchToolWidget()
assetImporterTool.setToolPath("/Game/Y24/Tools/W_AssetImporter")
assetImporterTool.init_entry(
    owner_name=tools_menu.menu_name,
    menu=tools_menu.menu_name,
    section="AssetManagement",
    name = "AssetImporter",
    label = "Asset Importer",
    tool_tip = "Click to open Asset Importer Tool"
)
assetImporterTool.register_menu_entry()

#Search Replace Name Tool
animImporterTool = LaunchToolWidget()
animImporterTool.setToolPath("/Game/Y24/Tools/W_AnimationImporter")
animImporterTool.init_entry(
    owner_name=tools_menu.menu_name,
    menu=tools_menu.menu_name,
    section="AssetManagement",
    name = "AnimImporterTool",
    label = "Import Animations",
    tool_tip = "Click to import animations from groups/shrineflow/assets/Animation"
)
animImporterTool.register_menu_entry()

#Search Replace Name Tool
searchReplaceNameTool = LaunchToolWidget()
searchReplaceNameTool.setToolPath("/Game/Y24/Tools/W_SearchReplaceName")
searchReplaceNameTool.init_entry(
    owner_name=tools_menu.menu_name,
    menu=tools_menu.menu_name,
    section="AssetManagement",
    name = "SearchReplaceName",
    label = "Search Replace Name",
    tool_tip = "Click to open Asset Search Replace Name Tool"
)
searchReplaceNameTool.register_menu_entry()

#Maya Camera Locator
mayaCameraLocator = LaunchToolWidget()
mayaCameraLocator.setToolPath("/Game/Y24/Tools/W_MayaCameraLocator")
mayaCameraLocator.init_entry(
    owner_name=tools_menu.menu_name,
    menu=tools_menu.menu_name,
    section="AssetManagement",
    name = "MayaCameraLocator",
    label = "Maya Camera Locator",
    tool_tip = "Click to set character camera positions for Maya"
)
mayaCameraLocator.register_menu_entry()

