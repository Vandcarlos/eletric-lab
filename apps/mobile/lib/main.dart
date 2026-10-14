import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;
import 'package:image_picker/image_picker.dart';

void main() => runApp(const EletricLabApp());

class EletricLabApp extends StatelessWidget {
  const EletricLabApp({super.key});

  @override
  Widget build(BuildContext context) => MaterialApp(
    title: 'Eletric Lab',
    theme: ThemeData(useMaterial3: true, colorSchemeSeed: Colors.teal),
    home: const InspectionScreen(),
  );
}

class InspectionScreen extends StatefulWidget {
  const InspectionScreen({super.key});

  @override
  State<InspectionScreen> createState() => _InspectionScreenState();
}

class _InspectionScreenState extends State<InspectionScreen> {
  bool loading = false;
  String result = 'Selecione uma fotografia para iniciar.';
  static const apiBase = String.fromEnvironment(
    'API_BASE_URL', defaultValue: 'http://127.0.0.1:8000');

  Future<void> inspect() async {
    final image = await ImagePicker().pickImage(source: ImageSource.gallery);
    if (image == null) return;
    setState(() { loading = true; result = 'Enviando imagem...'; });
    try {
      final request = http.MultipartRequest('POST', Uri.parse('$apiBase/v1/inspections'));
      request.files.add(await http.MultipartFile.fromPath('image', image.path));
      final response = await http.Response.fromStream(await request.send());
      if (response.statusCode != 201) {
        throw Exception('Erro HTTP ${response.statusCode}: ${response.body}');
      }
      final data = jsonDecode(response.body) as Map<String, dynamic>;
      setState(() {
        result = '${data['summary']}\n\nObservações:\n'
            '${(data['observations'] as List).join('\n')}\n\n'
            'Informações necessárias:\n'
            '${(data['required_information'] as List).join('\n')}\n\n'
            'Limitações:\n${(data['limitations'] as List).join('\n')}';
      });
    } catch (error) {
      setState(() => result = 'Falha na comunicação: $error');
    } finally {
      if (mounted) setState(() => loading = false);
    }
  }

  @override
  Widget build(BuildContext context) => Scaffold(
    appBar: AppBar(title: const Text('Eletric Lab')),
    body: Padding(
      padding: const EdgeInsets.all(20),
      child: Column(crossAxisAlignment: CrossAxisAlignment.stretch, children: [
        const Text('Inspeção assistida (MVP)', style: TextStyle(fontSize: 22)),
        const SizedBox(height: 12),
        const Text('Este protótipo não analisa visualmente a imagem nem certifica segurança.'),
        const SizedBox(height: 24),
        FilledButton.icon(
          onPressed: loading ? null : inspect,
          icon: const Icon(Icons.photo_library_outlined),
          label: Text(loading ? 'Aguarde...' : 'Selecionar fotografia'),
        ),
        const SizedBox(height: 20),
        Expanded(child: SingleChildScrollView(child: SelectableText(result))),
      ]),
    ),
  );
}
