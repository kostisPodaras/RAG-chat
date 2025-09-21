# TODO List

## File Upload & Document Management

### High Priority
- [ ] **Add duplicate file detection** - Prevent uploading same file twice (filename check)
- [ ] **Implement content-based deduplication** - Hash file content to detect identical files with different names
- [ ] **ChromaDB deduplication** - Prevent duplicate text chunks in vector database
- [ ] **User feedback for duplicates** - Warn users when file already exists with option to replace

### Technical Implementation
- [ ] Add file hash calculation during upload
- [ ] Check existing filenames before saving
- [ ] Query ChromaDB for existing content hashes
- [ ] Add replace/skip options in upload UI
- [ ] Clean up orphaned ChromaDB chunks when files are deleted

## Future Enhancements

### User Management
- [ ] Add user authentication system
- [ ] Implement per-user session isolation
- [ ] Consider document sharing vs isolation policies

### Performance
- [ ] Optimize ChromaDB queries for large document sets
- [ ] Add document search and filtering
- [ ] Implement document tagging/categorization