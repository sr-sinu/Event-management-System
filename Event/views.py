from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from django.utils.timezone import now
from .models import Event, Attendee
from .serializers import EventSerializer, AttendeeSerializer
from rest_framework.parsers import FileUploadParser
import csv
from rest_framework.permissions import IsAuthenticated

class EventListCreateView(ListCreateAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        status_filter = self.request.query_params.get('status')
        location_filter = self.request.query_params.get('location')
        date_filter = self.request.query_params.get('date')

        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if location_filter:
            queryset = queryset.filter(location__icontains=location_filter)
        if date_filter:
            queryset = queryset.filter(start_time__date=date_filter)
        return queryset

class EventDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAuthenticated]

    def perform_update(self, serializer):
        event = self.get_object()
        if event.end_time < now():
            serializer.validated_data['status'] = 'completed'
        serializer.save()


class RegisterAttendeeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = AttendeeSerializer(data=request.data)
        if serializer.is_valid():
            event = Event.objects.get(id=serializer.validated_data['event'].id)
            if event.attendees.count() >= event.max_attendees:
                return Response({"error": "Event is fully booked."}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CheckInAttendeeView(APIView):
    def post(self, request, attendee_id):
        try:
            attendee = Attendee.objects.get(pk=attendee_id)
            attendee.check_in_status = True
            attendee.save()
            return Response({"message": "Attendee checked in successfully."}, status=status.HTTP_200_OK)
        except Attendee.DoesNotExist:
            return Response({"error": "Attendee not found."}, status=status.HTTP_404_NOT_FOUND)


class ListAttendeesView(APIView):
    def get(self, request, event_id):
        attendees = Attendee.objects.filter(event_id=event_id)
        check_in_status = request.query_params.get('check_in_status')
        if check_in_status is not None:
            attendees = attendees.filter(check_in_status=check_in_status.lower() == 'true')
        serializer = AttendeeSerializer(attendees, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class BulkCheckInView(APIView):
    parser_classes = [FileUploadParser]

    def post(self, request):
        file_obj = request.FILES['file']
        try:
            decoded_file = file_obj.read().decode('utf-8').splitlines()
            reader = csv.DictReader(decoded_file)

            for row in reader:
                attendee = Attendee.objects.get(email=row['email'])
                attendee.check_in_status = True
                attendee.save()

            return Response({"message": "Bulk check-in successful."}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
