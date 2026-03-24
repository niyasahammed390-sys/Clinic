import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      home: LoginPage(),
    );
  }
}

class LoginPage extends StatefulWidget {
  @override
  _LoginPageState createState() => _LoginPageState();
}

class _LoginPageState extends State<LoginPage> {
  final TextEditingController username = TextEditingController();
  final TextEditingController password = TextEditingController();

  String message = "";

  Future<void> login() async {
    final url = Uri.parse("https://clinic-vxma.onrender.com/login/");

    final response = await http.post(
    url,
    headers: {"Content-Type": "application/json"},
    body: jsonEncode({
      "username": username.text,
      "password": password.text,
    }),
  );

  print("STATUS: ${response.statusCode}");
  print("BODY: ${response.body}");


    final data = jsonDecode(response.body);

  if (data["status"] == "success") {
    Navigator.push(
      context,
      MaterialPageRoute(builder: (context) => Dashboard()),
    );
  } else {
    setState(() {
      message = data["message"] ?? "Login failed";
    });
  }
}

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Center(
        child: Container(
          padding: EdgeInsets.all(20),
          width: 300,
          child: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text("Clinic Login", style: TextStyle(fontSize: 22)),
              SizedBox(height: 20),

              TextField(
                controller: username,
                decoration: InputDecoration(labelText: "Username"),
              ),

              TextField(
                controller: password,
                obscureText: true,
                decoration: InputDecoration(labelText: "Password"),
              ),

              SizedBox(height: 20),

              ElevatedButton(
                onPressed: login,
                child: Text("Login"),
              ),

              SizedBox(height: 10),
              Text(message, style: TextStyle(color: Colors.red)),
            ],
          ),
        ),
      ),
    );
  }
}

class Dashboard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Dashboard")),
      body: Center(
        child: Text("Welcome to Clinic App 🎉"),
      ),
    );
  }
}