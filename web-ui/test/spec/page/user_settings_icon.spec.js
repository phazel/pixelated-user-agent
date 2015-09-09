describeComponent('page/user_settings_icon', function () {
    'use strict';

    describe('user settings icon', function () {
        var features;

        beforeEach(function() {
            features = require('features');
        });

        it('should provide user settings icon', function () {
            spyOn(features, 'isLogoutEnabled').and.returnValue(true);

            this.setupComponent('<nav id="user-settings-icon"></nav>', {});

            var user_settings_icon = this.component.$node.find('a')[0];
            expect(user_settings_icon).toExist();
        });

        it('should still provide user settings icon if logout is disabled', function() {
            spyOn(features, 'isLogoutEnabled').and.returnValue(false);

            this.setupComponent('<nav id="user-settings-icon"></nav>', {});

            var user_settings_icon = this.component.$node.find('a')[0];
            expect(user_settings_icon).toExist();
        });
    });
});