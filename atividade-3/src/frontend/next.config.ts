import type { NextConfig } from "next";

// Exportado como site estático e servido pelo próprio FastAPI: um link só.
const config: NextConfig = {
  output: "export",
  trailingSlash: true,
  images: { unoptimized: true },
};

export default config;
