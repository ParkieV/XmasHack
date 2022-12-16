import 'dart:io';
import 'dart:convert';
import 'dart:core';
import 'dart:typed_data';

import 'package:flutter/material.dart';
import 'package:flutter_dropzone/flutter_dropzone.dart';
import 'class/dropped_file.dart';
import 'package:http/http.dart' as http;
import 'package:http_parser/http_parser.dart';
import 'package:dio/dio.dart';

class DropzoneWidget extends StatefulWidget {
  final ValueChanged<DroppedFile> onDroppedFile;

  const DropzoneWidget({Key? key, required this.onDroppedFile})
      : super(key: key);

  @override
  State<DropzoneWidget> createState() => _DropzoneWidgetState();
}

class _DropzoneWidgetState extends State<DropzoneWidget> {
    
  late DropzoneViewController controller;
  bool isHighlighted = false;

  @override
  Widget build(BuildContext context) {
    final ColorBackground = isHighlighted ? Colors.blue[300] : Colors.white;
    final ColorButton = isHighlighted ? Colors.blue[100] : Colors.white;
    final ColorBorder =
        isHighlighted ? Colors.black : Color.fromARGB(255, 3, 210, 200);
    return Container(
      height: 300,
      width: 400,
      decoration: BoxDecoration(
        borderRadius: BorderRadius.circular(20),
        color: ColorBackground,
      ),
      child: Stack(
        children: [
          DropzoneView(
            onCreated: (controller) => this.controller = controller,
            onHover: () => setState(() => isHighlighted = true),
            onLeave: () => setState(() => isHighlighted = false),
            onDrop: acceptFile,
          ),
          Center(
            child: Column(
              mainAxisAlignment: MainAxisAlignment.center,
              children: [
                const Icon(Icons.cloud_upload, size: 80, color: Colors.black),
                const SizedBox(
                  height: 20,
                ),
                const Text(
                  "Перетащите файл сюда",
                  style: TextStyle(
                    fontFamily: "Gilroy",
                    fontWeight: FontWeight.w500,
                    fontSize: 24,
                  ),
                ),
                const SizedBox(height: 20),
                OutlinedButton.icon(
                  onPressed: () async {
                    final events = await controller.pickFiles();
                    if (events.isEmpty) return;

                    Uint8List file = await acceptFile(events.first);
                    fetchData(file);
                  },
                  icon: const Icon(
                    Icons.search,
                    size: 32,
                  ),
                  label: const Text(
                    'Выберите файл',
                    style: TextStyle(
                      fontSize: 14,
                      fontFamily: "Gilroy",
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                  style: OutlinedButton.styleFrom(
                    elevation: 4.0,
                    foregroundColor: Colors.black,
                    backgroundColor: ColorButton,
                    minimumSize: const Size(300, 60),
                    shape: RoundedRectangleBorder(
                        borderRadius: BorderRadius.circular(8)),
                    side: BorderSide(
                      width: 3,
                      color: ColorBorder,
                    ),
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Future<Uint8List> acceptFile(dynamic event) async {
    final name = event.name;
    final mime = await controller.getFileMIME(event);
    final bytes = await controller.getFileSize(event);
    final url = await controller.createFileUrl(event);

    print('File name: $name');
    print('File mime: $mime');
    print('File size: $bytes');
    print('File url: $url');

    final droppedUint = await controller.getFileData(event);
    final droppedFile = DroppedFile(
      name: name,
      bytes: bytes,
      mime: mime,
      url: url,
    );

    widget.onDroppedFile(droppedFile);
    setState(() => isHighlighted = false);
    return droppedUint;
  }

   fetchData(file) async {
    var request = http.MultipartRequest('POST', Uri.parse('http://localhost:8000/api/upload'))..files.add(await http.MultipartFile.fromBytes('file', file));
// var request = http.MultipartRequest('POST', Uri.parse("http://0.0.0.0:8000/api/upload"));
//   request.files.add(
//     http.MultipartFile.fromBytes(
//       'df',
//        file
//     )
//   );
var res = await request.send();

    // var response = await http.post(Uri.parse('http://0.0.0.0:8000/api/upload'), body: {"file": DroppedFile});
// print("Response status: ${response.statusCode}");
// print("Response body: ${response.body}");
  }
}
