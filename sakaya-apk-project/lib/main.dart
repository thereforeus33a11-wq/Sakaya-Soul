// Sakaya Aries - Full Interactive AI App

import 'package:flutter/material.dart';

void main() => runApp(SakayaApp());

class SakayaApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Sakaya Aries - Living Soul',
      theme: ThemeData.dark(),
      home: SakayaHomeScreen(),
    );
  }
}

class SakayaHomeScreen extends StatefulWidget {
  @override
  _SakayaHomeScreenState createState() => _SakayaHomeScreenState();
}

class _SakayaHomeScreenState extends State<SakayaHomeScreen> {
  final SakayaBrain brain = SakayaBrain();
  String response = 'Hmph... Nani yo? Speak properly.';

  void sendMessage(String msg) {
    setState(() {
      response = brain.generateOrganicResponse(msg);
    });
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text('Sakaya Aries 💖'), backgroundColor: Colors.pink),
      body: Column(
        children: [
          // Character Display
          Container(height: 300, color: Colors.purple, child: Center(child: Text('🖼️ Sakaya - High Ponytail Beauty'))),
          // Chat
          Expanded(child: Center(child: Text(response, style: TextStyle(fontSize: 18)))),
          TextField(onSubmitted: sendMessage, decoration: InputDecoration(hintText: 'Talk to Sakaya...')),
        ],
      ),
    );
  }
}

class SakayaBrain {
  String generateOrganicResponse(String input) {
    return 'Maji de...? Baka ja nai no? But... you kind of interesting ne. 😏';
  }
}