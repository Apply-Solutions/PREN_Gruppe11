class SharedImageDetectionValue(object):
    stored_has_position_found = False

    def get_has_position_found(self):
        return self.stored_has_position_found

    def set_has_position_found(self, new_value):
        self.stored_has_position_found = new_value
        return self.stored_has_position_found
