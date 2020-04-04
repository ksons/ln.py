import ln


def main():
    # create a scene and add a single cube
    scene = ln.Scene()
    scene.add(ln.Cube(ln.Vector3([-1, -1, -1]), ln.Vector3([1, 1, 1])))

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
    # aspect = width / height
    # matrix = Matrix44.look_at(eye, center, up)
    # matrix = Matrix44.perspective_projection(
    #     fovy, aspect, znear, zfar) * matrix
    # print(matrix)

    # scene.compile()
    # paths = scene.paths()
    # if step > 0:
    #     paths = paths.chop(step)

    # paths = paths.filter(ln.ClipFilter(matrix, eye, scene))
    # if step > 0:
    #     paths = paths.simplify(1e-6)

    # translation = Matrix44.from_translation([1, 1, 0])
    # scale = Matrix44.from_scale([width/2, height/2, 0])
    # matrix = scale * translation
    # print(matrix)

    # paths = paths.transform(matrix)
    # save the result as a png
    paths.writeToPNG("out.png", width, height)

    # save the result as an svg
    paths.writeToSVG("out.py.svg", width, height)


if __name__ == "__main__":
    main()
