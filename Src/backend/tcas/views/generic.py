class PermissionDictMixin:
    """
    Mixin to select permission class from the variable `permission_set` in viewsets
    """

    def get_permissions(self):
        perm_list = self.permission_dict[self.action] if self.action in self.permission_dict else self.permission_dict['others']
        return [perm() for perm in perm_list]
