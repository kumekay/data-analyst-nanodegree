use Rack::Static,
  :urls => ["/assets_1", "/assets", "/data", "/data_v1"],
  :root => "."

run lambda { |env|
  [
    200,
    {
      'Content-Type'  => 'text/html',
      'Cache-Control' => 'public, max-age=86400'
    },
    File.open('index_1.html', File::RDONLY)
  ]
}
