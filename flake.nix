{
  inputs = {
    utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, utils }: utils.lib.eachDefaultSystem (system:
    let
      pkgs = nixpkgs.legacyPackages.${system};
      pythonPackages = pkgs.python312Packages;
    in
    {
      devShell = pkgs.mkShell rec {
        venvDir = "./.venv";
        NIX_LD = builtins.readFile "${pkgs.stdenv.cc}/nix-support/dynamic-linker";
        NIX_LD_LIBRARY_PATH = pkgs.lib.makeLibraryPath buildInputs;


        buildInputs = with pkgs; [
          pythonPackages.python
          pythonPackages.tkinter
          pythonPackages.pip
          pythonPackages.wheel
          pythonPackages.venvShellHook

          stdenv.cc.cc
          zlib
        ];

        postVenvCreation = /* bash */
          ''
            pip install -r requirements.txt
          '';

        postShellHook = /* bash */
          ''
            export LD_LIBRARY_PATH=$NIX_LD_LIBRARY_PATH:$LD_LIBRARY_PATH
          '';
      };
    }
  );
}
