{
  inputs = {
    utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, utils }: utils.lib.eachDefaultSystem (system:
    let
      pythonOverlay = final: prev: { python312 = prev.python312.override { x11Support = true; }; };
      pkgs = import nixpkgs { overlays = [ pythonOverlay ]; };
      pythonPackages = pkgs.python312Packages;
    in
    {
      devShell = pkgs.mkShell {
        venvDir = "./.venv";

        buildInputs = with pkgs; [
          pythonPackages.python
          pythonPackages.pip
          pythonPackages.wheel
          pythonPackages.venvShellHook

          stdenv.cc.cc
          openssl
          libffi
          libpqxx
          freetype
          libjpeg
          git
          zlib
          openssl
          postgresql
          curl
          gcc
          jdk21
          maven
          jdt-language-server
        ];

        postVenvCreation = /* bash */
          ''
            pip install requirements.txt
          '';
      };
    }
  );
}
