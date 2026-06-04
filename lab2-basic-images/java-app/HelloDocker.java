import com.sun.net.httpserver.HttpServer;
import com.sun.net.httpserver.HttpHandler;
import com.sun.net.httpserver.HttpExchange;

import java.io.IOException;
import java.io.OutputStream;
import java.net.InetSocketAddress;
import java.time.Instant;

/**
 * Lab 2 — Java HTTP Server
 * A simple HTTP server using Java's built-in HttpServer (no extra dependencies).
 *
 * Build:  javac HelloDocker.java
 * Run:    java HelloDocker
 */
public class HelloDocker {

    static final int PORT = 8080;

    public static void main(String[] args) throws IOException {
        HttpServer server = HttpServer.create(new InetSocketAddress(PORT), 0);

        server.createContext("/", new RootHandler());
        server.createContext("/health", new HealthHandler());
        server.setExecutor(null);

        System.out.println("=== Java Docker App ===");
        System.out.println("Server running on port " + PORT);
        System.out.println("JVM: " + System.getProperty("java.version"));
        System.out.println("OS:  " + System.getProperty("os.name"));
        System.out.println("Container hostname: " + System.getenv("HOSTNAME"));
        System.out.println("=======================");

        server.start();
    }

    static class RootHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String hostname = System.getenv("HOSTNAME") != null
                    ? System.getenv("HOSTNAME") : "unknown";

            String response = "{\n" +
                "  \"message\": \"Hello from Java inside Docker!\",\n" +
                "  \"java_version\": \"" + System.getProperty("java.version") + "\",\n" +
                "  \"os\": \"" + System.getProperty("os.name") + "\",\n" +
                "  \"architecture\": \"" + System.getProperty("os.arch") + "\",\n" +
                "  \"container_id\": \"" + hostname + "\",\n" +
                "  \"timestamp\": \"" + Instant.now() + "\"\n" +
                "}";

            sendResponse(exchange, 200, response);
        }
    }

    static class HealthHandler implements HttpHandler {
        @Override
        public void handle(HttpExchange exchange) throws IOException {
            String response = "{\n" +
                "  \"status\": \"healthy\",\n" +
                "  \"service\": \"java-hello-docker\",\n" +
                "  \"timestamp\": \"" + Instant.now() + "\"\n" +
                "}";
            sendResponse(exchange, 200, response);
        }
    }

    static void sendResponse(HttpExchange exchange, int code, String body) throws IOException {
        byte[] bytes = body.getBytes("UTF-8");
        exchange.getResponseHeaders().set("Content-Type", "application/json; charset=UTF-8");
        exchange.sendResponseHeaders(code, bytes.length);
        try (OutputStream os = exchange.getResponseBody()) {
            os.write(bytes);
        }
    }
}
