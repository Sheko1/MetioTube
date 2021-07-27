import time
from threading import Thread
from MetioTube.main_app.models import VideoView


def video_view_delete_session_key(video_view):
    time.sleep(30)
    video_view.session_key = ''
    video_view.save()


def get_view(request, video_pk):
    if not request.session.session_key:
        request.session.create()

    video_view_session_cd = VideoView.objects.filter(session_key=request.session.session_key, video_id=video_pk)

    if video_view_session_cd:
        return

    video_view = VideoView(
        video_id=video_pk,
        session_key=request.session.session_key
    )

    video_view.save()

    Thread(target=video_view_delete_session_key, args=(video_view,)).start()
