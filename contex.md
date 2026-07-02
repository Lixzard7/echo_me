# EchoMe - Project Context

## Project Overview

EchoMe is a real-time voice conversion application.

The goal is to capture microphone audio, convert it in real time using an RVC voice model, and output the converted audio to a virtual microphone so that applications like:

- Discord
- Google Meet
- Microsoft Teams
- Zoom
- OBS

hear the converted voice instead of the user's real voice.

The project should NOT depend on the Applio UI or W-Okada UI.

The project should only use their inference engine internally.

---

# Current Architecture

Current project contains:

Backend
- FastAPI
- WebSocket streaming
- Audio capture
- Audio playback

Client
- Captures microphone
- Sends PCM chunks over websocket
- Receives PCM chunks
- Plays converted audio

Streaming already works.

Current pipeline:

Mic
↓

Capture

↓

WebSocket

↓

Server

↓

Return PCM

↓

Speaker

Currently audio is simply passed through.

The missing part is replacing pass-through audio with RVC inference.

---

# Important Constraints

There is ONLY ONE voice model.

There is NO requirement to switch between models.

There is NO requirement for multiple users to have different models.

There is NO requirement for uploading models.

There is NO GUI.

There is NO model manager UI.

There is NO slot manager.

There is NO REST API for models.

Everything should be hardcoded for a single model.

---

# Users

Expected concurrent users:

5–15

NOT hundreds.

Latency is much more important than scalability.

---

# Existing Assets

Model:

backend/models/my_voice.pth

Index:

backend/models/my_voice.index

Hubert model will also exist locally.

RMVPE model will also exist locally.

Everything should be loaded automatically during startup.

---

# Desired Startup Flow

Server starts

↓

Load Hubert

↓

Load RMVPE

↓

Load my_voice.pth

↓

Load my_voice.index

↓

Create RVC pipeline

↓

Ready

The model should NEVER reload during runtime.

---

# Runtime Flow

Mic Audio

↓

WebSocket

↓

RVC Engine

↓

Converted PCM

↓

WebSocket

↓

Client Playback

Later this playback will be replaced by a virtual microphone.

---

# Current Goal

Completely remove dependence on:

- Applio Dashboard
- W-Okada GUI

Use ONLY their backend inference code.

---

# W-Okada Usage

We are NOT rewriting W-Okada.

We are ONLY borrowing the inference engine.

Ignore:

- GUI
- React
- Docker
- Trainer
- Slot Manager
- REST API
- VoiceChangerManager
- Upload System
- Settings UI
- Multiple Voice Models

Only inference matters.

---

# Files Already Copied

Several backend inference files from W-Okada already exist inside the project.

Do NOT copy the repository again.

Reuse existing code.

Remove unnecessary abstraction whenever possible.

---

# Required Simplification

Replace dynamic architecture with a fixed implementation.

Instead of:

load slot

↓

find model

↓

create manager

↓

create pipeline

↓

convert

Use:

startup:

engine = RVCEngine(
    model="backend/models/my_voice.pth",
    index="backend/models/my_voice.index"
)

During websocket:

converted = engine.convert(audio)

Nothing more.

---

# Performance Goal

Realtime conversion.

Target latency:

Under 100 ms.

Never reload models.

Never recreate pipeline.

Everything remains in GPU memory.

---

# Virtual Microphone

Current output:

Speaker playback.

Future output:

Virtual microphone driver.

Pipeline should therefore output raw PCM.

Do NOT mix playback logic with inference.

---

# What Needs To Be Implemented

The agent should inspect the codebase and identify where audio is currently passed through unchanged.

Replace pass-through with RVC inference.

If there is already a partially implemented inference engine, complete it rather than creating another one.

---

# Refactoring Rules

Keep existing project structure.

Do NOT introduce unnecessary managers.

Do NOT introduce unnecessary abstraction.

Do NOT create another architecture layer.

Prefer direct code.

Example:

Bad

WebSocket
↓

Service
↓

Manager
↓

Converter
↓

Engine
↓

Pipeline

Good

WebSocket
↓

RVCEngine.convert()

↓

Return PCM

---

# Coding Style

Simple.

Readable.

Production-ready.

Avoid excessive design patterns.

Avoid unnecessary dependency injection.

Avoid singleton abuse unless absolutely necessary.

---

# Final Deliverable

A working backend where:

1. FastAPI starts.
2. RVC model loads once.
3. Audio chunks are converted.
4. Converted PCM is returned.
5. Existing websocket streaming continues to work.
6. No Applio UI.
7. No W-Okada UI.
8. No dashboard.
9. Only EchoMe backend.

---

# IMPORTANT
    
Before writing new code, inspect the existing project.

If an implementation already exists, complete it instead of rewriting it.

Minimize duplicate code.

Reuse existing files.

Avoid creating parallel implementations.

The objective is a clean, maintainable codebase with a single RVC inference pipeline.
Read PROJECT_CONTEXT.md first.

Then inspect the ENTIRE codebase before making any changes.

Do not generate new architecture.

Find the existing websocket pipeline and the existing RVC inference code.

Reuse as much existing code as possible.

Complete the implementation so that microphone PCM sent through the websocket is converted using backend/models/my_voice.pth and backend/models/my_voice.index.

Do not use Applio UI or W-Okada UI.

Keep the existing project structure.

Return complete replacement files whenever modifications are needed instead of partial code snippets.

Do not stop after analysis—implement the required changes.