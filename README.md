# Bober Stack 🦫
### LausHack 2024 - BOBST Challenge Project

## Overview
Bober Stack is a full-stack monitoring and control system developed for BOBST packaging company during LausHack 2024. The project name comes from "bober" (beaver) - our mascot representing BOBST's connection to paper and cardboard packaging.

The system provides real-time control and monitoring of a miniature Arduino-operated packaging conveyor belt through a Raspberry Pi interface.

## Architecture
![Architecture Diagram Placeholder]()
- Angular Frontend for user interface
- Spring Boot Backend API
- Prometheus for metrics collection
- Python service on Raspberry Pi
- Arduino-controlled conveyor belt

## Features
- **Real-time Control Panel**
 - 5-step speed control (10-14 units)
 - Power management
 - System status monitoring

   <br>
 
- **Live Metrics Dashboard**: PU usage and frequency, Memory utilization,  Disk usage, System load, Custom application metrics
   
    <br>

- **Alert System**: Real-time system alerts, Multiple severity levels, Visual indicators, Configurable alert rules
   
    <br>

- **Logging Interface**: System events tracking, Operation logs, Error monitoring
   
    <br>

- **BOBST Platform Integration**: Direct access to BOBST operator equipment portal

## Tech Stack
### Frontend
- Angular 17
- TypeScript
- Angular Material UI
- Chart.js
- SCSS

### Backend
- Java 17
- Spring Boot
- Prometheus
- Docker
- Maven

### IoT
- Python
- Raspberry Pi
- Arduino

## Setup Instructions

### Prerequisites
- Node.js and npm
- Java 17
- Maven
- Docker
- Python 3
- Raspberry Pi
- Arduino setup

### Frontend Setup
1. Install dependencies:
```bash
npm install
