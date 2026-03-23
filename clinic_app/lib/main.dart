import 'dart:convert';
import 'package:flutter/material.dart';
import 'package:http/http.dart' as http;

void main() {
  runApp(const MyApp());
}

class MyApp extends StatelessWidget {
  const MyApp({super.key});

  @override
  Widget build(BuildContext context) {
    return MaterialApp(
      debugShowCheckedModeBanner: false,
      title: 'Clinic App',
      theme: ThemeData(
        primarySwatch: Colors.blue,
      ),
      home: const PatientPage(),
    );
  }
}

class PatientPage extends StatefulWidget {
  const PatientPage({super.key});

  @override
  State<PatientPage> createState() => _PatientPageState();
}

class _PatientPageState extends State<PatientPage> {
  List patients = [];
  bool isLoading = true;

  @override
  void initState() {
    super.initState();
    fetchPatients();
  }

  // 🔥 FETCH DATA FROM YOUR DJANGO API
  fetchPatients() async {
    try {
      final response = await http.get(
        Uri.parse('https://clinic-vxma.onrender.com/api/patients/'),
      );

      print(response.body); // Debug

      if (response.statusCode == 200) {
        setState(() {
          patients = json.decode(response.body);
          isLoading = false;
        });
      } else {
        throw Exception('Failed to load patients');
      }
    } catch (e) {
      print("Error: $e");
      setState(() {
        isLoading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text("Patients"),
        centerTitle: true,
      ),

      // 🔥 BODY
      body: isLoading
          ? const Center(child: CircularProgressIndicator())
          : patients.isEmpty
              ? const Center(child: Text("No Patients Found"))
              : ListView.builder(
                  itemCount: patients.length,
                  itemBuilder: (context, index) {
                    final p = patients[index];

                    return Card(
                      margin: const EdgeInsets.symmetric(
                          horizontal: 10, vertical: 5),
                      elevation: 3,
                      child: ListTile(
                        leading: CircleAvatar(
                          child: Text(p['name'][0]),
                        ),
                        title: Text(p['name']),
                        subtitle: Text(
                          "Age: ${p['age']} | Phone: ${p['phone'] ?? ''}",
                        ),
                      ),
                    );
                  },
                ),
    );
  }
}