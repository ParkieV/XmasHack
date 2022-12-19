import 'package:flutter/material.dart';
import 'package:google_fonts/google_fonts.dart';
import 'package:xmasfront/components/class/dropped_file.dart';
import 'package:xmasfront/components/dropped_file_widget.dart';
import 'package:xmasfront/components/dropzone_widget.dart';

class HomePage extends StatefulWidget {
  @override
  _HomePageState createState() => _HomePageState();
}

class _HomePageState extends State<HomePage> {
  DroppedFile? file;

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(
        crossAxisAlignment: CrossAxisAlignment.center,
        // ignore: prefer_const_literals_to_create_immutables
        children: [
          Column(
            children: [
              const SizedBox(height: 60),
              Padding(
                padding: const EdgeInsets.symmetric(horizontal: 50),
                child: Column(
                  // ignore: prefer_const_literals_to_create_immutables
                  children: [
                    const Center(
                      child: Text(
                        "M I S I S    A T L A N T I S",
                        style: TextStyle(
                          fontSize: 30,
                          fontFamily: 'Gilroy',
                          fontWeight: FontWeight.w700,
                        ),
                      ),
                    ),
                  ],
                ),
              ),
              const SizedBox(
                height: 60,
              ),
              Material(
                elevation: 4.0,
                borderRadius: BorderRadius.circular(20),
                child: SizedBox(
                  height: 200,
                  width: 400,
                  child: Container(
                    alignment: const Alignment(0, -0.75),
                    child: Column(
                      mainAxisAlignment: MainAxisAlignment.center,
                      // ignore: prefer_const_literals_to_create_immutables
                      children: [
                        const SizedBox(
                          height: 20,
                        ),
                        const Text(
                          "Добро пожаловать!",
                          style: TextStyle(
                            fontSize: 30,
                            fontFamily: 'Gilroy',
                            fontWeight: FontWeight.w700,
                          ),
                        ),
                        const SizedBox(
                          height: 10,
                        ),
                        const Padding(
                          padding: EdgeInsets.symmetric(horizontal: 15),
                          child: Text(
                            "Для начала работы импортируйте файл типа doc, docx, pdf",
                            textAlign: TextAlign.center,
                            style: TextStyle(
                              fontSize: 16,
                              fontFamily: 'Gilroy',
                              fontWeight: FontWeight.w400,
                              color: Color(0xFF8F8F8F),
                            ),
                          ),
                        ),
                        const SizedBox(
                          height: 20,
                        ),
                      ],
                    ),
                  ),
                ),
              ),
              const SizedBox(
                height: 30,
              ),
              Material(
                elevation: 4.0,
                borderRadius: BorderRadius.circular(20),
                child: DropzoneWidget(
                    onDroppedFile: (file) => setState(() => this.file = file)),
              ),
              const SizedBox(
                height: 30,
              ),
              DroppedFileWidget(
                file: file,
              ),
              const SizedBox(
                height: 90,
              ),
              Container(
                height: 60,
                child: Image.asset(
                  "ITAM.png",
                ),
              )
            ],
          ),
        ],
      ),
    );
  }
}
