import 'package:flutter/material.dart';
import 'package:xmasfront/pages/result.dart';
import 'class/dropped_file.dart';

class DroppedFileWidget extends StatelessWidget {
  final DroppedFile? file;

  const DroppedFileWidget({Key? key, this.file}) : super(key: key);

  @override
  Widget build(BuildContext context) => Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          if (file != null) buildFileDetails(file!, context),
        ],
      );

  Widget buildText() {
    if (file == null) return buildEmptyFile('Нет файлов');
    return Image.network(
      file!.url,
      width: 120,
      height: 120,
      fit: BoxFit.cover,
      errorBuilder: (context, error, _) => buildEmptyFile(''),
    );
  }

  Widget buildEmptyFile(String text) => Material(
        elevation: 4.0,
        borderRadius: BorderRadius.circular(20),
        child: Container(
          width: 300,
          height: 100,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(20),
            color: Colors.white,
          ),
          child: Center(
            child: Text(
              text,
              style: const TextStyle(
                fontSize: 14,
                fontWeight: FontWeight.w500,
              ),
            ),
          ),
        ),
      );

  Widget buildFileDetails(DroppedFile file, BuildContext context) {
    // ignore: prefer_const_declarations
    final style = const TextStyle(
      fontSize: 14,
    );

    return Material(
      color: Colors.white,
      elevation: 4.0,
      borderRadius: BorderRadius.circular(20),
      child: Column(
        children: [
          Container(
            // text center
            height: 50,
            width: 350,
            margin: const EdgeInsets.only(left: 20),
            child: Row(
              mainAxisAlignment: MainAxisAlignment.start,
              children: [
                const Icon(
                  Icons.file_present,
                  size: 40,
                  color: Colors.black,
                ),
                const SizedBox(width: 10),
                Center(
                  child: Text(
                    file.name,
                    style: style.copyWith(
                      fontWeight: FontWeight.w500,
                    ),
                  ),
                ),
              ],
            ),
          ),
          OutlinedButton.icon(
            onPressed: () {
              Navigator.push(
                context,
                MaterialPageRoute(builder: (context) => const ResultPage()),
              );
            },
            icon: const Icon(Icons.chevron_right_rounded),
            label: const Text('Далее'),
            style: OutlinedButton.styleFrom(
              elevation: 4.0,
              foregroundColor: Colors.black,
              backgroundColor: Colors.white,
              minimumSize: const Size(120, 40),
              shape: RoundedRectangleBorder(
                borderRadius: BorderRadius.circular(8),
              ),
              side: const BorderSide(
                color: Color.fromARGB(255, 191, 89, 255),
                width: 3,
              ),
            ),
          ),
          const SizedBox(
            height: 10,
          ),
        ],
      ),
    );
  }
}
