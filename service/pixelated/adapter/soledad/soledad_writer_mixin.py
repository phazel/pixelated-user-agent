#
# Copyright (c) 2014 ThoughtWorks, Inc.
#
# Pixelated is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pixelated is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with Pixelated. If not, see <http://www.gnu.org/licenses/>.
from pixelated.adapter.soledad.soledad_facade_mixin import SoledadDbFacadeMixin

from twisted.internet import defer


class SoledadWriterMixin(SoledadDbFacadeMixin, object):

    @defer.inlineCallbacks
    def mark_all_as_not_recent(self):
        for mailbox in ['INBOX', 'DRAFTS', 'SENT', 'TRASH']:
            rct = yield self.get_recent_by_mbox(mailbox)
            if not rct or not rct[0].content['rct']:
                return
            rct = rct[0]
            rct.content['rct'] = []
            yield self.put_doc(rct)

    def save_mail(self, mail):
        return self.put_doc(mail.fdoc)

    @defer.inlineCallbacks
    def create_mail(self, mail, mailbox_name):
        mbox_doc = (yield self.get_mbox(mailbox_name))[0]
        uid = 1 + (yield self.get_lastuid(mbox_doc))

        yield self.create_docs(mail.get_for_save(next_uid=uid, mailbox=mailbox_name))

        # FIXME need to update meta message (mdoc)
        # mbox_doc.content['lastuid'] = uid + 1
        # self.put_doc(mbox_doc)

        defer.returnValue((yield self.mail(mail.ident)))

    @defer.inlineCallbacks
    def remove_mail(self, mail):
        # FIX-ME: Must go through all the part_map phash to delete all the cdocs
        yield self.delete_doc(mail.fdoc)
        yield self.delete_doc(mail.hdoc)
        yield self.delete_doc(mail.bdoc)
