def vec2px(renderer, v):
    return (
        int(v.x),
        int(v.y - renderer.camera.y)
    )
