#！/usr/bin/env python
#! -*-coding:utf-8 -*-
#!@Author : zhuxx
#!@time : 2020/04/24 19:50

from PIL import Image

titles = '图像对比测试结果'

def title():
    title = '''<!DOCTYPE html>
	<html lang="en">
	<head>
		<meta charset="UTF-8">
		<title>%s</title>
		<style>
              @font-face {
                  font-family: 'latoregular';
                  src: url('./assets/fonts/lato-regular-webfont.woff2') format('woff2'),
                      url('./assets/fonts/lato-regular-webfont.woff') format('woff');
                  font-weight: 400;
                  font-style: normal;
              }
              @font-face {
                  font-family: 'latobold';
                  src: url('./assets/fonts/lato-bold-webfont.woff2') format('woff2'),
                      url('./assets/fonts/lato-bold-webfont.woff') format('woff');
                  font-weight: 700;
                  font-style: normal;
              }

              .ReactModal__Body--open {
                  overflow: hidden;
              }
              .ReactModal__Body--open .header {
                display: none;
              }
        </style>
	</head>
	<body style="background-color: #E2E7EA">
	    <div id="root">

    </div>
    <script type="text/javascript">
      function report (report) { // eslint-disable-line no-unused-vars
        window.tests = report;
      }
    </script>
	''' % (titles)
    return title


def creat_js(script):
    js = '''
        <script type="text/javascript">
		report({
		  "testSuite": "视觉测试",
		  "tests": [
			%s
		  ],
		  "id": "默认模板"
		});
	</script>
	<script type="text/javascript" src="index_bundle.js"></script>
  </body>
</html>
    ''' % (script)
    return js


def script_true(reference_pic, test_pic, file_name, isSameDimensions, status):
    script1 = '''
    {
      "pair": {
        "reference": "..\\\\bitmaps_reference\\\\%s",
        "DB": "..\\\\bitmaps_test\\\\%s",
        "selector": "文件",
        "fileName": "%s",
        "label": "主页",
        "requireSameDimensions": true,
        "misMatchThreshold": 0.1,
        "diff": {
          "isSameDimensions": %s,
          "dimensionDifference": {
            "width": 0,
            "height": 0
          },
          "misMatchPercentage": "0.00"
        }
      },
      "status": "%s"
    },
    ''' % (reference_pic, test_pic, file_name, isSameDimensions, status)
    return script1


def script(reference_pic, test_pic, file_name, isSameDimensions, x, y, size, diff_pic, status):
    script1 = '''
        {
          "pair": {
            "reference": "..\\\\bitmaps_reference\\\\%s",
            "DB": "..\\\\bitmaps_test\\\\%s",
            "selector": "文件",
            "fileName": "%s",
            "label": "主页",
            "requireSameDimensions": true,
            "misMatchThreshold": 0.1,
            "diff": {
              "isSameDimensions": %s,
              "dimensionDifference": {
                "width": %s,
                "height": %s
              },
              "misMatchPercentage": "%s",
              "analysisTime": 46
            },
            "diffImage": "..\\\\diff_image\\\\%s"
          },
          "status": "%s"
        },
    ''' % (reference_pic, test_pic, file_name, isSameDimensions, x, y, size, diff_pic, status)
    return script1


script1 = ""


def createHTML(file,reference_pic, diff_pic, test_pic, file_name, html_filepath, isSameDimensions, status, info):
    global script1
    # print(reference_pic,diff_pic,test_pic,file_name,html_filepath,isSameDimensions,status)
    if status == "pass":
        script1 = script1 + script_true(reference_pic, test_pic, file_name, isSameDimensions, status)
    else:
        size = Image.open(file + "\\bitmaps_reference\\" + reference_pic).size
        crop_size = (info[2] - info[0]) * (info[3] - info[1])
        size1 = crop_size / (size[0] * size[1]) * 100
        script1 = script1 + script(reference_pic, test_pic, file_name, isSameDimensions, info[0], info[1],
                                   "%.2f" % size1, diff_pic, status)
    tests = title() + creat_js(script1)
    with open(html_filepath, 'wb') as f:
        f.write(tests.encode("utf-8"))

