from django.core.management.base import BaseCommand

from verification_token.models import VerificationToken


class Command(BaseCommand):
    help = "Clean inactive and expired verification tokens."

    def add_arguments(self, parser):
        # Named (optional) arguments
        parser.add_argument(
            "--inactive",
            action="store_true",
            help="Delete only verification tokens which are inactive "
            + "(is_active = False)",
        )
        parser.add_argument(
            "--expired",
            action="store_true",
            help="Delete only verification tokens which are expired "
            + "(expiry_date_lte = timezone.now())",
        )

    def handle(self, *args, **options):
        if options["inactive"] or options["expired"]:
            VerificationToken.objects.clean_invalid_tokens(
                clean_inactive=options["inactive"], clean_expired=options["expired"]
            )
        else:
            VerificationToken.objects.clean_invalid_tokens()
