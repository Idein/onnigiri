{
  description = "onnigiri";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-21.11";
    flake-utils.url = "github:numtide/flake-utils";
  };
  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        py = pkgs.python38;
        packageName = "onnigiri";
        customOverrides = self: super: rec {
            platformdirs = py.pkgs.platformdirs;
        };
      in
      {
        packages.${packageName} = pkgs.poetry2nix.mkPoetryApplication {
          projectDir = ./.;
          python = py;
          overrides = [ pkgs.poetry2nix.defaultPoetryOverrides customOverrides ];
          preferWheels = true;
        };

        defaultPackage = self.packages.${system}.${packageName};

        devShell = pkgs.mkShell {
          buildInputs = [
            pkgs.protobuf

            py
            py.pkgs.jedi-language-server
            py.pkgs.poetry
          ];

          inputsFrom = builtins.attrValues self.packages.${system};

          shellHook = ''
            export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [ pkgs.stdenv.cc.cc ]}
          '';
        };
      }
    );
}
