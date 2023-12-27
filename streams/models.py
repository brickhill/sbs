from wagtail import blocks
from wagtail.images.blocks import ImageChooserBlock


class TitleBlock(blocks.StructBlock):
    text = blocks.CharBlock(
        required=True,
        help_text="Text to display"
    )

    class Meta:
        template = "streams/title_block.html"
        icon = "edit"
        label = "Title"
        help_text = "Centred text to display on the page"


class CardsBlock(blocks.StructBlock):
    cards = blocks.ListBlock(
        blocks.StructBlock([
            ("title", blocks.CharBlock(max_length=100,
                                       help_text="Bold title text (max 100)")),
            ("text", blocks.TextBlock(max_length=255,
                                      help_text="Optional text, max 255", required=False)),
            ("image", ImageChooserBlock(
                help_text="Image will be cropped to 570px x 370px"))
        ]
        )
    )

    class Meta:
        template = "streams/cards_block.html"
        icon = "image"
        label = "Cards"
        help_text = "Cards"
