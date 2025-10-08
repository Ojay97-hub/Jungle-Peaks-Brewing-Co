from django.core.management.base import BaseCommand
from django.db import models
from checkout.models import Order


class Command(BaseCommand):
    help = 'Recalculate order totals for orders containing tours or taproom bookings'

    def add_arguments(self, parser):
        parser.add_argument(
            '--dry-run',
            action='store_true',
            help='Show what would be updated without making changes',
        )

    def handle(self, *args, **options):
        dry_run = options['dry_run']

        # Find orders that have line items with tour bookings or taproom bookings
        orders_to_update = Order.objects.filter(
            models.Q(lineitems__tour_booking__isnull=False) |
            models.Q(lineitems__taproom_booking__isnull=False)
        ).distinct()

        if not orders_to_update.exists():
            self.stdout.write(
                self.style.SUCCESS('No orders with tours or taproom bookings found.')
            )
            return

        self.stdout.write(
            f'Found {orders_to_update.count()} orders with tours or taproom bookings to recalculate'
        )

        updated_count = 0
        for order in orders_to_update:
            old_total = order.order_total
            old_grand_total = order.grand_total

            # Recalculate the total
            order.update_total()

            if order.order_total != old_total or order.grand_total != old_grand_total:
                updated_count += 1
                if dry_run:
                    self.stdout.write(
                        f'  Order {order.order_number}: '
                        f'{old_total} -> {order.order_total} '
                        f'(Grand: {old_grand_total} -> {order.grand_total})'
                    )
                else:
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'  Updated Order {order.order_number}: '
                            f'{old_total} -> {order.order_total} '
                            f'(Grand: {old_grand_total} -> {order.grand_total})'
                        )
                    )
            else:
                self.stdout.write(
                    f'  Order {order.order_number}: No change needed'
                )

        if dry_run:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Dry run complete. {updated_count} orders with tours or taproom bookings would be updated.'
                )
            )
        else:
            self.stdout.write(
                self.style.SUCCESS(
                    f'Successfully updated {updated_count} orders with tours or taproom bookings.'
                )
            )
