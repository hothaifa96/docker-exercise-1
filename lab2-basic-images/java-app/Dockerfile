# ============================================================
# Lab 2 — Java Dockerfile (Multi-Stage Build)
# Concept: Multi-stage builds to minimize final image size
# ============================================================

# ── STAGE 1: builder ─────────────────────────────────────────
# We need the FULL JDK to compile Java source code
# This stage is called "builder" — we reference it below
FROM openjdk:17-slim AS builder

LABEL maintainer="Docker Labs"
LABEL description="Stage 1: Compile Java source"

WORKDIR /compile

# COPY just the source file(s) to compile
COPY HelloDocker.java .

# RUN javac to compile .java → .class
# The .class file is the bytecode the JVM runs
RUN javac HelloDocker.java

# ── STAGE 2: runtime ─────────────────────────────────────────
# The final image — uses a SMALLER JRE (no compiler, no javac)
# JDK (~400 MB) vs JRE (~200 MB) — multi-stage saves ~200 MB!
FROM openjdk:17-slim

LABEL description="Stage 2: Run compiled Java app"

WORKDIR /app

# KEY INSTRUCTION: COPY --from=builder
# Copies only the compiled .class file from the builder stage
# The source code (HelloDocker.java) is NOT in this final image
COPY --from=builder /compile/HelloDocker.class .

EXPOSE 8080

# CMD runs the compiled class (no .class extension needed)
CMD ["java", "HelloDocker"]
