{
  description = "onnigiri";
  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
    poetry2nix = {
      url = "github:nix-community/poetry2nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };
  outputs = { self, nixpkgs, flake-utils, poetry2nix }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        inherit (poetry2nix.lib.mkPoetry2Nix { inherit pkgs; }) mkPoetryApplication overrides;
        pkgs = nixpkgs.legacyPackages.${system};
        py = pkgs.python39;
        packageName = "onnigiri";
        customOverrides = self: super: {
          platformdirs = super.platformdirs.overridePythonAttrs (
            old: {
              postPatch = "";
            }
          );

          onnxruntime = super.onnxruntime.overridePythonAttrs (
            old: {
              nativeBuildInputs = [ ];
              postFixup =
                let rPath = pkgs.lib.makeLibraryPath [ pkgs.stdenv.cc.cc ];
                in
                ''
                  rrPath=${rPath}
                  find $out/lib -name '*.so' -exec patchelf --add-rpath "$rrPath" {} \;
                '';
            }
          );
        };
      in
      {
        packages.${packageName} = mkPoetryApplication {
          projectDir = ./.;
          python = py;
          overrides = overrides.withDefaults (
            customOverrides
          );
          preferWheels = true;
        };

        packages.dockerimage = pkgs.dockerTools.buildImage {
          name = "idein/${packageName}";
          tag = "latest";
          created = "now";
          copyToRoot = [ self.packages.${system}.${packageName} ];
          config = {
            Entrypoint = [ "/bin/onnigiri" ];
            WorkingDir = "/work";
          };
        };

        defaultPackage = self.packages.${system}.${packageName};

        devShell = pkgs.mkShell {
          buildInputs = [
            pkgs.protobuf

            py
            pkgs.poetry
          ];

          inputsFrom = builtins.attrValues self.packages.${system};

          shellHook = ''
            export LD_LIBRARY_PATH=${pkgs.lib.makeLibraryPath [ pkgs.stdenv.cc.cc ]}
          '';
        };
      }
    );
}
