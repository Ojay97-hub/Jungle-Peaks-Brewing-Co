"""Email utility functions for booking confirmations.

This module provides functions to send confirmation emails for:
- Taproom table reservations
- Brewery tour bookings
"""

import logging
from django.conf import settings
from django.core.mail import send_mail
from django.template.loader import render_to_string

logger = logging.getLogger(__name__)

# Booking type display names
TAPROOM_BOOKING_TYPES = {
    'standard': 'Standard Table Reservation',
    'premium': 'Premium Table Reservation',
}

TOUR_TYPES = {
    'guided': 'Guided Brewery Tour',
    'sunset': 'Sunset Tour',
    'craft_tasting': 'Craft Beer Tasting',
    'seasonal': 'Seasonal Selection',
    'brewer_session': 'Master Brewer Session',
}


def _get_from_email():
    """Return the configured sender address."""
    return getattr(settings, 'DEFAULT_FROM_EMAIL', 'noreply@junglepeaksbrewing.com')


def send_taproom_booking_confirmation(booking, booking_type='standard'):
    """Send confirmation email for a taproom table reservation.
    
    Args:
        booking: The Booking model instance
        booking_type: 'standard' or 'premium'
    
    Returns:
        1 on success, 0 on failure
    """
    context = {
        'booking': booking,
        'booking_type_display': TAPROOM_BOOKING_TYPES.get(booking_type, 'Table Reservation'),
        'contact_email': _get_from_email(),
    }
    
    subject = render_to_string(
        'emails/taproom_booking_subject.txt', context
    ).strip()
    body = render_to_string(
        'emails/taproom_booking_body.txt', context
    )
    
    try:
        sent = send_mail(
            subject=subject,
            message=body,
            from_email=_get_from_email(),
            recipient_list=[booking.email],
            fail_silently=False
        )
        logger.info(
            "Taproom booking confirmation sent to %s for booking on %s",
            booking.email, booking.date
        )
        print(f"✅ Taproom booking confirmation sent to {booking.email}")
        return sent
    except Exception as e:
        logger.error(
            "Failed to send taproom booking confirmation to %s: %s",
            booking.email, str(e)
        )
        print(f"❌ Failed to send taproom confirmation: {str(e)}")
        return 0


def send_tour_booking_confirmation(booking):
    """Send confirmation email for a brewery tour booking.
    
    Args:
        booking: The TourBooking model instance
    
    Returns:
        1 on success, 0 on failure
    """
    context = {
        'booking': booking,
        'tour_display': TOUR_TYPES.get(booking.tour, booking.tour),
        'contact_email': _get_from_email(),
    }
    
    subject = render_to_string(
        'emails/tour_booking_subject.txt', context
    ).strip()
    body = render_to_string(
        'emails/tour_booking_body.txt', context
    )
    
    try:
        sent = send_mail(
            subject=subject,
            message=body,
            from_email=_get_from_email(),
            recipient_list=[booking.email],
            fail_silently=False
        )
        logger.info(
            "Tour booking confirmation sent to %s for %s on %s",
            booking.email, booking.tour, booking.date
        )
        print(f"✅ Tour booking confirmation sent to {booking.email}")
        return sent
    except Exception as e:
        logger.error(
            "Failed to send tour booking confirmation to %s: %s",
            booking.email, str(e)
        )
        print(f"❌ Failed to send tour confirmation: {str(e)}")
        return 0
