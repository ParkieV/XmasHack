import 'package:flutter/material.dart';
import 'class/dropped_file.dart';

class DroppedFileWidget extends StatelessWidget {
  final DroppedFile? file;

  const DroppedFileWidget({Key? key, this.file}) : super(key: key);

  @override
  Widget build(BuildContext context) => Row(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          if (file != null) buildFileDetails(file!),
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
          width: 400,
          height: 120,
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

  Widget buildFileDetails(DroppedFile file) {
    // ignore: prefer_const_declarations
    final style = const TextStyle(
      fontSize: 14,
    );

    return Material(
      elevation: 4.0,
      borderRadius: BorderRadius.circular(20),
      child: Container(
        // text center
        height: 100,
        width: 400,
        margin: const EdgeInsets.only(left: 20),
        child: Row(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              Icons.file_present,
              size: 40,
              color: Colors.black,
            ),
            const SizedBox(width: 20),
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
    );
  }
}
