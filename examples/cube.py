import ln


def main():
    # create a scene and add a single cube
    scene = ln.Scene()
    scene.add(ln.Cube([-1, -1, -1], [1, 1, 1]))

    # define camera parameters
    eye = ln.Vector3([4, 3, 2])  # camera position
    center = ln.Vector3([0, 0, 0])  # camera looks at
    up = ln.Vector3([0, 0, 1])  # up direction

    # define rendering parameters
    width = 1024  # rendered width
    height = 1024  # rendered height
    fovy = 50.0  # vertical field of view, degrees
    znear = 0.1  # near z plane
    zfar = 10.0  # far z plane
    step = 0.01  # how finely to chop the paths for visibility testing

    # compute 2D paths that depict the 3D scene
    paths = scene.Render(eye, center, up, width, height,
                         fovy, znear, zfar, step)

    # save the result as a png
    paths.writeToPNG("out.png", width, height)

    # save the result as an svg
    paths.writeToSVG("out.py.svg", width, height)


if __name__ == "__main__":
    main()
