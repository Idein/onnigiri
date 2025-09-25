{
  description = "onnigiri";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        py = pkgs.python311;
      in
      {
        devShell = pkgs.mkShell {
          buildInputs = [
            pkgs.protobuf

            py
            pkgs.poetry
          ];

          # shellHook = ''
          #   export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [ pkgs.stdenv.cc.cc ]}
          # '';
        };
      }
    );
}
