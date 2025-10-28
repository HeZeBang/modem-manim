{
  inputs = {
    flake-parts.url = "github:hercules-ci/flake-parts";
    nixpkgs.url = "github:NixOS/nixpkgs/nixpkgs-unstable";
    treefmt-nix = {
      url = "github:numtide/treefmt-nix";
      inputs.nixpkgs.follows = "nixpkgs";
    };
  };

  outputs =
    inputs@{ flake-parts, treefmt-nix, ... }:
    flake-parts.lib.mkFlake { inherit inputs; } {
      imports = [
        treefmt-nix.flakeModule
      ];
      systems = [ "aarch64-darwin" ];
      perSystem =
        { pkgs, ... }:
        {
          devShells.default = pkgs.mkShell {
            nativeBuildInputs = with pkgs; [
              ffmpeg
              pkg-config
              (texliveBasic.withPackages (
                ps: with ps; [
                  dvisvgm
                  preview
                  standalone
                ]
              ))
              uv
            ];

            buildInputs = with pkgs; [
              cairo
            ];
          };

          treefmt = {
            projectRootFile = "flake.nix";
            programs = {
              black.enable = true;
              nixfmt.enable = true;
            };
          };
        };
    };
}
