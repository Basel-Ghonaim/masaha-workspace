-- AlterTable
ALTER TABLE "announcements" ADD COLUMN     "request_id" UUID NOT NULL;

-- CreateIndex
CREATE UNIQUE INDEX "announcements_space_id_request_id_key" ON "announcements"("space_id", "request_id");

