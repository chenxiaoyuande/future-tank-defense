package main
var savedProgress string
var unavailable bool
func storageRead() (string,bool) {return savedProgress,!unavailable}
func storageWrite(raw string) bool {if unavailable{return false};savedProgress=raw;return true}
func backupProgress(raw string) {}
func restoreProgress() string {return ""}
