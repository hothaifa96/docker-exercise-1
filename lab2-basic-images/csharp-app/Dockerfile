FROM mcr.microsoft.com/dotnet/sdk:8.0 as builder

WORKDIR /app

COPY DockerApp.csproj .

RUN dotnet restore DockerApp.csproj

COPY . .

RUN dotnet publish DockerApp.csproj \
-c Release \
-o /app/publish \
--no-restore


FROM mcr.microsoft.com/dotnet/aspnet:8.0

WORKDIR /app

ENV PORT=8080

COPY --from=builder /app/publish ./

EXPOSE 8080

CMD ["dotnet","DockerApp.dll"]