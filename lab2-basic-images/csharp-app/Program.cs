// Lab 2 — C# ASP.NET Core Minimal API
// A lightweight web API using .NET 8 minimal API style

using System.Runtime.InteropServices;

var builder = WebApplication.CreateBuilder(args);

// Read environment variable set in Dockerfile / docker run
var appVersion = Environment.GetEnvironmentVariable("APP_VERSION") ?? "1.0";
var environment = Environment.GetEnvironmentVariable("ASPNETCORE_ENVIRONMENT") ?? "Production";

var app = builder.Build();

// Route 1: Root
app.MapGet("/", () => Results.Ok(new
{
    message   = "Hello from C# ASP.NET Core inside Docker!",
    version   = appVersion,
    environment,
    container = Environment.MachineName,
    timestamp = DateTime.UtcNow.ToString("o")
}));

// Route 2: Detailed info
app.MapGet("/info", () => Results.Ok(new
{
    runtime       = RuntimeInformation.FrameworkDescription,
    os            = RuntimeInformation.OSDescription,
    architecture  = RuntimeInformation.ProcessArchitecture.ToString(),
    hostname      = Environment.MachineName,
    dotnet_version = Environment.Version.ToString(),
    app_version   = appVersion,
    environment
}));

// Route 3: Health check
app.MapGet("/health", () => Results.Ok(new
{
    status    = "healthy",
    service   = "csharp-aspnet-demo",
    timestamp = DateTime.UtcNow.ToString("o")
}));

var port = Environment.GetEnvironmentVariable("PORT") ?? "8080";
Console.WriteLine($"=== C# Docker App ===");
Console.WriteLine($"Version: {appVersion}");
Console.WriteLine($"Runtime: {RuntimeInformation.FrameworkDescription}");
Console.WriteLine($"Listening on port {port}");
Console.WriteLine($"=====================");

app.Run($"http://0.0.0.0:{port}");
