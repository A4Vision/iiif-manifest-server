import copy
from collections import namedtuple
from typing import List, Dict

SAMPLE_WORKSPACE = {
    "annotationBodyEditor": {
        "module": "TinyMCEAnnotationBodyEditor",
        "options": {
            "config": {
                "plugins": "image link media directionality",
                "toolbar": "bold italic | bullist numlist | link image media | removeformat | ltr rtl"
            }
        }
    },
    "annotationEndpoint": {
        "module": "LocalStorageEndpoint",
        "name": "Local Storage"
    },
    "autoHideControls": True,
    "availableAnnotationDrawingTools": [
        "Rectangle",
        "Ellipse",
        "Freehand",
        "Polygon",
        "Pin"
    ],
    "availableAnnotationModes": [],
    "availableAnnotationStylePickers": [
        "StrokeColor",
        "FillColor",
        "StrokeType"
    ],
    "availableCanvasTools": [],
    "availableExternalCommentsPanel": False,
    "buildPath": "./assets/mirador/",
    "data": [],
    "drawingToolsSettings": {
        "doubleClickReactionTime": 300,
        "fillColor": "deepSkyBlue",
        "fillColorAlpha": 0,
        "fixedShapeSize": 10,
        "hoverColor": "yellow",
        "newlyCreatedShapeStrokeWidthFactor": 5,
        "shapeHandleSize": 10,
        "strokeColor": "deepSkyBlue"
    },
    "eventEmitter": {
        "debug": False,
        "debugExclude": [],
        "emitterId": 1,
        "trace": False
    },
    "fadeDuration": 400,
    "i18nPath": "locales/",
    "id": "viewer",
    "imagesPath": "images/",
    "jsonStorageEndpoint": {
        "module": "JSONBlobAPI",
        "name": "JSONBlob API Endpoint",
        "options": {
            "host": "jsonblob.com",
            "port": "443",
            "ssl": True
        }
    },
    "layout": "{\"type\":\"row\",\"depth\":0,\"value\":0,\"x\":3,\"y\":3,\"dx\":1043,\"dy\":668,\"address\":\"row1\",\"id\":\"eb32d641-7dec-413f-819b-5c8c0b543475\"}",
    "lockController": {
        "lockProfile": "lazyZoom",
        "notifyMaxMin": True
    },
    "mainMenuSettings": {
        "buttons": {
            "bookmark": False,
            "fullScreenViewer": True,
            "layout": True,
            "options": False
        },
        "show": True,
        "userButtons": [
            {
                "attributes": {
                    "class": "desktop-open"
                },
                "iconClass": "fa fa-lg fa-fw fa-picture-o",
                "label": "Open"
            },
            {
                "attributes": {
                    "class": "desktop-publish"
                },
                "iconClass": "fa fa-lg fa-fw fa-newspaper-o",
                "label": "Publish"
            },
            {
                "attributes": {
                    "class": "desktop-import"
                },
                "iconClass": "fa fa-lg fa-fw fa-upload",
                "label": "Import"
            },
            {
                "attributes": {
                    "class": "desktop-export"
                },
                "iconClass": "fa fa-lg fa-fw fa-download",
                "label": "Export"
            }
        ],
        "userLogo": {
            "iconClass": "fa fa-lg fa-fw fa-sliders",
            "label": "Mirador Desktop"
        }
    },
    "manifestPanelVisible": True,
    "manifests": [],
    "openManifestsPage": True,
    "preserveManifestOrder": False,
    "saveSession": False,
    "shapeHandleSize": 10,
    "sharingEndpoint": {
        "APIKey": "23983hf98j3f9283jf2983fj",
        "storeId": 123,
        "url": ""
    },
    "showAddFromURLBox": True,
    "sidePanelOptions": {
        "layersTabAvailable": True,
        "searchTabAvailable": True,
        "tocTabAvailable": True
    },
    "timeoutDuration": 3000,
    "windowObjects": [],
    "windowSettings": {
        "availableViews": [
            "ThumbnailsView",
            "ImageView",
            "ScrollView",
            "BookView"
        ],
        "bottomPanel": True,
        "bottomPanelVisible": True,
        "canvasControls": {
            "annotations": {
                "annotationCreation": True,
                "annotationLayer": True,
                "annotationRefresh": False,
                "annotationState": "off"
            },
            "imageManipulation": {
                "controls": {
                    "brightness": True,
                    "contrast": True,
                    "grayscale": True,
                    "invert": True,
                    "rotate": True,
                    "saturate": True
                },
                "manipulationLayer": True
            }
        },
        "displayLayout": True,
        "fullScreen": True,
        "layoutOptions": {
            "close": True,
            "newObject": True,
            "slotAbove": True,
            "slotBelow": True,
            "slotLeft": True,
            "slotRight": True
        },
        "overlay": True,
        "sidePanel": True,
        "sidePanelOptions": {
            "annotations": False,
            "layersTabAvailable": True,
            "searchTabAvailable": False,
            "toc": True,
            "tocTabAvailable": True
        },
        "sidePanelVisible": True,
        "viewType": "ImageView"
    },
    "workspacePanelSettings": {
        "maxColumns": 5,
        "maxRows": 5,
        "preserveWindows": True
    },
    "workspaceType": "singleObject",
    "workspaces": {
        "bookReading": {
            "addNew": True,
            "defaultWindowOptions": {},
            "iconClass": "book",
            "label": "Book Reading",
            "move": False
        },
        "compare": {
            "iconClass": "columns",
            "label": "Compare"
        },
        "singleObject": {
            "addNew": False,
            "iconClass": "image",
            "label": "Single Object",
            "move": False
        }
    }
}

ManifestSpec = namedtuple("ManifestSpec", "uri location")


def create_workspace(manifests_spec: List[ManifestSpec]) -> Dict:
    d = copy.deepcopy(SAMPLE_WORKSPACE)
    d['data'] = [{'manifestUri': s.uri, 'location': s.location} for s in manifests_spec]
    return d
