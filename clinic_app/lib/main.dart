import 'package:flutter/material.dart';
import 'dart:convert';
import 'package:http/http.dart' as http;

void main() {
  runApp(MyApp());
}

class MyApp extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      title: 'Clinic App',
      theme: ThemeData(primarySwatch: Colors.blue),
      home: PatientScreen(),
    );
  }
}

class PatientScreen extends StatefulWidget {
  @override
  _PatientScreenState createState() => _PatientScreenState();
}

class _PatientScreenState extends State<PatientScreen> {
  List patients = [];

  @override
  void initState() {
    super.initState();
    fetchPatients();
  }

  fetchPatients() async {
    final response = await http.get(
      Uri.parse('https://clinic-vxma.onrender.com/api/patients/')
    );

    if (response.statusCode == 200) {
      setState(() {
        patients = json.decode(response.body);
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: Text("Patients")),
      body: patients.isEmpty
          ? Center(child: CircularProgressIndicator())
          : ListView.builder(
              itemCount: patients.length,
              itemBuilder: (context, index) {
                return Card(
                  margin: EdgeInsets.all(10),
                  child: ListTile(
                    title: Text(patients[index]['name']),
                    subtitle: Text("Phone: ${patients[index]['phone']}"),
                  ),
                );
              },
            ),
    );
  }
}