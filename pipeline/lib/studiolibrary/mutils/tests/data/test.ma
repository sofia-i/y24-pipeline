//Maya ASCII 2013 scene
//Name: test.ma
//Last modified: Thu, Jun 26, 2014 01:46:47 PM
//Codeset: UTF-8
requires maya "2013";
currentUnit -l centimeter -a degree -t film;
fileInfo "application" "maya";
fileInfo "product" "Maya 2013";
fileInfo "version" "2013 Service Pack 2P12 x64";
fileInfo "cutIdentifier" "201304120319-868747";
fileInfo "osv" "Linux 3.5.4-2.10-desktop #1 SMP PREEMPT Fri Oct 5 14:56:49 CEST 2012 x86_64";
createNode animCurveTA -n "DELETE_NODE_rotateX";
	addAttr -ci true -sn "fullname" -ln "fullname" -dt "string";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 45 10 30.81018202226841;
	setAttr -k on ".fullname" -type "string" "srcSphere:sphere.rotateX";
createNode animCurveTU -n "DELETE_NODE_testEnum";
	addAttr -ci true -sn "fullname" -ln "fullname" -dt "string";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 1 10 1;
	setAttr -s 2 ".kot[0:1]"  5 5;
	setAttr -k on ".fullname" -type "string" "srcSphere:sphere.testEnum";
createNode animCurveTL -n "DELETE_NODE_translateX";
	addAttr -ci true -sn "fullname" -ln "fullname" -dt "string";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0 10 0;
	setAttr -k on ".fullname" -type "string" "srcSphere:sphere.translateX";
createNode animCurveTL -n "DELETE_NODE_translateY";
	addAttr -ci true -sn "fullname" -ln "fullname" -dt "string";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 8 10 8;
	setAttr -k on ".fullname" -type "string" "srcSphere:sphere.translateY";
createNode animCurveTL -n "DELETE_NODE_translateZ";
	addAttr -ci true -sn "fullname" -ln "fullname" -dt "string";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 -12 10 11.214436147065292;
	setAttr -k on ".fullname" -type "string" "srcSphere:sphere.translateZ";
createNode animCurveTA -n "DELETE_NODE_rotateY";
	addAttr -ci true -sn "fullname" -ln "fullname" -dt "string";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 25 10 -82.269409864294204;
	setAttr -k on ".fullname" -type "string" "srcSphere:sphere.rotateY";
createNode animCurveTU -n "DELETE_NODE_testFloat";
	addAttr -ci true -sn "fullname" -ln "fullname" -dt "string";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0.666 10 0.666;
	setAttr -k on ".fullname" -type "string" "srcSphere:sphere.testFloat";
createNode animCurveTU -n "DELETE_NODE_testAnimated";
	addAttr -ci true -sn "fullname" -ln "fullname" -dt "string";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0 10 10;
	setAttr -k on ".fullname" -type "string" "srcSphere:sphere.testAnimated";
createNode animCurveTU -n "DELETE_NODE_scaleX";
	addAttr -ci true -sn "fullname" -ln "fullname" -dt "string";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0.25 10 0.42958527814637792;
	setAttr -k on ".fullname" -type "string" "srcSphere:sphere.scaleX";
createNode animCurveTU -n "DELETE_NODE_scaleY";
	addAttr -ci true -sn "fullname" -ln "fullname" -dt "string";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 1.5 10 2.5775116688782669;
	setAttr -k on ".fullname" -type "string" "srcSphere:sphere.scaleY";
createNode animCurveTU -n "DELETE_NODE_visibility";
	addAttr -ci true -sn "fullname" -ln "fullname" -dt "string";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 1 10 1;
	setAttr -s 2 ".kot[0:1]"  5 5;
	setAttr -k on ".fullname" -type "string" "srcSphere:sphere.visibility";
createNode animCurveTU -n "DELETE_NODE_testVectorX";
	addAttr -ci true -sn "fullname" -ln "fullname" -dt "string";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0.2 10 0.2;
	setAttr -k on ".fullname" -type "string" "srcSphere:sphere.testVectorX";
createNode animCurveTU -n "DELETE_NODE_testVectorY";
	addAttr -ci true -sn "fullname" -ln "fullname" -dt "string";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 1.4 10 1.4;
	setAttr -k on ".fullname" -type "string" "srcSphere:sphere.testVectorY";
createNode animCurveTA -n "DELETE_NODE_rotateZ";
	addAttr -ci true -sn "fullname" -ln "fullname" -dt "string";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 90 10 149.70880463068096;
	setAttr -k on ".fullname" -type "string" "srcSphere:sphere.rotateZ";
createNode animCurveTU -n "DELETE_NODE_testVectorZ";
	addAttr -ci true -sn "fullname" -ln "fullname" -dt "string";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 2.6 10 2.6;
	setAttr -k on ".fullname" -type "string" "srcSphere:sphere.testVectorZ";
createNode animCurveTU -n "DELETE_NODE_scaleZ";
	addAttr -ci true -sn "fullname" -ln "fullname" -dt "string";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 0.5 10 0.85917055629275585;
	setAttr -k on ".fullname" -type "string" "srcSphere:sphere.scaleZ";
createNode animCurveTU -n "DELETE_NODE_testInteger";
	addAttr -ci true -sn "fullname" -ln "fullname" -dt "string";
	setAttr ".tan" 18;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 5 10 5;
	setAttr -k on ".fullname" -type "string" "srcSphere:sphere.testInteger";
createNode animCurveTU -n "DELETE_NODE_testBoolean";
	addAttr -ci true -sn "fullname" -ln "fullname" -dt "string";
	setAttr ".tan" 9;
	setAttr ".wgt" no;
	setAttr -s 2 ".ktv[0:1]"  1 1 10 1;
	setAttr -s 2 ".kot[0:1]"  5 5;
	setAttr -k on ".fullname" -type "string" "srcSphere:sphere.testBoolean";
select -ne :time1;
	setAttr -k on ".cch";
	setAttr -k on ".nds";
	setAttr ".o" 10;
	setAttr ".unw" 10;
select -ne :renderPartition;
	setAttr -k on ".cch";
	setAttr -k on ".nds";
	setAttr -s 2 ".st";
select -ne :initialShadingGroup;
	setAttr -k on ".cch";
	setAttr -k on ".nds";
	setAttr -s 2 ".dsm";
	setAttr -k on ".mwc";
	setAttr ".ro" yes;
select -ne :initialParticleSE;
	setAttr -k on ".cch";
	setAttr -k on ".nds";
	setAttr -k on ".mwc";
	setAttr ".ro" yes;
select -ne :defaultShaderList1;
	setAttr -k on ".cch";
	setAttr -k on ".nds";
	setAttr -s 2 ".s";
select -ne :postProcessList1;
	setAttr -k on ".cch";
	setAttr -k on ".nds";
	setAttr -s 2 ".p";
select -ne :defaultRenderingList1;
	setAttr -s 3 ".r";
select -ne :renderGlobalsList1;
	setAttr -k on ".cch";
	setAttr -k on ".nds";
select -ne :defaultResolution;
	setAttr -k on ".cch";
	setAttr -k on ".nds";
	setAttr -av ".w";
	setAttr -av ".h";
	setAttr -k on ".pa" 1;
	setAttr -k on ".al";
	setAttr -av ".dar";
	setAttr -k on ".ldar";
	setAttr -k on ".off";
	setAttr -k on ".fld";
	setAttr -k on ".zsl";
select -ne :defaultLightSet;
	setAttr -k on ".cch";
	setAttr -k on ".nds";
	setAttr -k on ".mwc";
	setAttr ".ro" yes;
select -ne :hardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -k on ".nds";
	setAttr ".ctrs" 256;
	setAttr ".btrs" 512;
select -ne :hardwareRenderingGlobals;
	setAttr ".otfna" -type "stringArray" 18 "NURBS Curves" "NURBS Surfaces" "Polygons" "Subdiv Surfaces" "Particles" "Fluids" "Image Planes" "UI:" "Lights" "Cameras" "Locators" "Joints" "IK Handles" "Deformers" "Motion Trails" "Components" "Misc. UI" "Ornaments"  ;
	setAttr ".otfva" -type "Int32Array" 18 0 1 1 1 1 1
		 1 0 0 0 0 0 0 0 0 0 0 0 ;
select -ne :defaultHardwareRenderGlobals;
	setAttr -k on ".cch";
	setAttr -k on ".nds";
	setAttr ".fn" -type "string" "im";
	setAttr ".res" -type "string" "ntsc_4d 646 485 1.333";
// End of test.ma
