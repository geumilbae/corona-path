import getpass

from rest_framework import permissions


def get_user_pwd(username: str):
    """이 함수를 호출하면 사용자명과 패스워드를 키보드에서 입력받아 튜플로 리턴합니다.

    :param username: 사용자명을 외부에서 파라메터로 입력받습니다.
    :type: str

    :return: (사용자명, 패스워드) 형태의 튜플
    :rtype: tuple
    """
    pwd = getpass.getpass()
    return username, pwd


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True

        return obj.user == request.user

