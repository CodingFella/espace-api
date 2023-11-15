<html>
<head>
<title>Run my Python files</title>
<?PHP
echo shell_exec("pip install -r requirements.txt")
echo shell_exec("KEY=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6ImFubmllLmhzdUByb2xjYy5uZXQiLCJodHRwOi8vc2NoZW1hcy54bWxzb2FwLm9yZy93cy8yMDA1LzA1L2lkZW50aXR5L2NsYWltcy9oYXNoIjoiOXIvREQ4UHhNVWhjYWhaTFpXdXdKSjFOZGNjPSIsIm5iZiI6MTY5OTkzMjc3NCwiZXhwIjoxNzMxNDY4Nzc0LCJpYXQiOjE2OTk5MzI3NzR9.gYLIlQqkbde_qJPPU2HGRmHNZtxI_xpNNNoJOogLdp4 python app.py");
?>
</head>