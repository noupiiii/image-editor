from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from fastapi.responses import JSONResponse
from app.services.image_utils import (
    extract_color_palette,
    transfer_colors_by_cluster,
    read_image_as_float,
    encode_image_to_base64,
)

router = APIRouter()

@router.post("/api/extract-colors/")
async def extract_colors(file: UploadFile = File(...), n_colors: int = Form(...)):
    """
    Extract the top `n_colors` from an uploaded image asynchronously.
    """
    if n_colors <= 0:
        raise HTTPException(status_code=400, detail="Number of colors must be greater than 0.")

    try:
        # Read the file into memory
        image_data = await file.read()

        # Use custom async function to extract palette
        hex_palette = await extract_color_palette(image_data, n_colors)

        return JSONResponse(content={"palette": hex_palette})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process image: {str(e)}")


@router.post("/transfert-colors/")
async def transfert_colors(
    fromFile: UploadFile = File(...),
    toFile: UploadFile = File(...),
    n_colors: int = Form(...)
):
    """
    Transfer colors from the source image to the target image asynchronously.
    """
    if n_colors <= 0:
        raise HTTPException(status_code=400, detail="Number of colors must be between 1 and 4.")

    try:
        # Read uploaded images
        from_image_data = await fromFile.read()
        to_image_data = await toFile.read()

        # Process images asynchronously
        source_image = await read_image_as_float(from_image_data)
        target_image = await read_image_as_float(to_image_data)

        # Perform color transfer asynchronously
        transferred_image = await transfer_colors_by_cluster(source_image, target_image, n_colors)

        # Encode the result in base64 asynchronously
        base64_image = await encode_image_to_base64(transferred_image)

        return JSONResponse(content={"transferred_image": f"data:image/png;base64,{base64_image}"})

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to process image: {str(e)}")
