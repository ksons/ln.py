import ln


def main():

    scene = ln.Scene()
    mesh = ln.load_obj("examples/suzanne.obj")
    mesh.unit_cube()

    scene.add(mesh)

    eye = ln.Vector3([2, 2, 2])
    center = ln.Vector3()
    up = ln.Vector3([0, 1, 0])

    # # define rendering parameters
    width = 1024  # rendered width
    height = 1024  # rendered height
    fovy = 35.0  # vertical field of view, degrees
    znear = 0.1  # near z plane
    zfar = 100.0  # far z plane
    step = 0.01  # how finely to chop the paths for visibility testing

    # # compute 2D paths that depict the 3D scene
    paths = scene.Render(eye, center, up, width, height,
                         fovy, znear, zfar, step)

    paths.writeToPNG("out.png", width, height)

    # save the result as an svg
    paths.writeToSVG("out.py.svg", width, height)


if __name__ == "__main__":
    main()
