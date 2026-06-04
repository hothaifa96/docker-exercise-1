# ============================================================
# Lab 2 — C# ASP.NET Core Dockerfile (Multi-Stage Build)
# Concept: Multi-stage with .NET SDK → ASP.NET runtime
# ============================================================

# ── STAGE 1: build ───────────────────────────────────────────
# Full .NET SDK — needed to compile and publish the app
# SDK image is ~720 MB — we don't want this in production!
FROM mcr.microsoft.com/dotnet/sdk:8.0 AS build

LABEL description="Stage 1: Build and publish C# app"

WORKDIR /src

# COPY .csproj file FIRST and restore packages
# Layer cache: if .csproj didn't change, NuGet restore is cached
COPY DockerApp.csproj .
RUN dotnet restore DockerApp.csproj

# COPY remaining source code
COPY . .

# Publish a self-contained release build
# Output goes to /app/publish
RUN dotnet publish DockerApp.csproj \
    -c Release \
    -o /app/publish \
    --no-restore

# ── STAGE 2: runtime ─────────────────────────────────────────
# ASP.NET runtime — ~220 MB (vs SDK at ~720 MB)
# Contains everything needed to RUN (not build) .NET apps
FROM mcr.microsoft.com/dotnet/aspnet:8.0

LABEL maintainer="Docker Labs"
LABEL app="csharp-aspnet-demo"
LABEL description="Stage 2: Run published C# app"

ENV APP_VERSION=1.0
ENV ASPNETCORE_ENVIRONMENT=Production
ENV PORT=8080

WORKDIR /app

# Copy only the published output from the build stage
# Source code, .csproj, and SDK are NOT in this image
COPY --from=build /app/publish .

EXPOSE 8080

# ENTRYPOINT — the dotnet runtime is always the executable
# Unlike CMD, ENTRYPOINT is not easily overridden
ENTRYPOINT ["dotnet", "DockerApp.dll"]
